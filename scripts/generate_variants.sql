-- SQL script to standardize original part_number to Bruto/Usinado
-- and create variant rows for each component in components_and_parts
BEGIN TRANSACTION;

-- helper CTEs for numbers
WITH RECURSIVE
  nums_br(n) AS (
    SELECT 2
    UNION ALL
    SELECT n+1 FROM nums_br WHERE n < 10
  ),
  nums_us(n) AS (
    SELECT 1
    UNION ALL
    SELECT n+1 FROM nums_us WHERE n < 20
  ),

  -- originals that are NOT "braço" special and not already suffixed
  origs AS (
    SELECT id,
           COALESCE(part_number, 'PN' || id) AS base,
           COALESCE(description, '') AS description,
           category, client_ID, supplier_ID, cost
    FROM components_and_parts
    WHERE lower(COALESCE(description,'')) NOT LIKE '%braço%'
      AND lower(COALESCE(description,'')) NOT LIKE '%pitman%'
      AND lower(COALESCE(part_number,'')) NOT LIKE '%-br-%'
      AND lower(COALESCE(part_number,'')) NOT LIKE '%-us-%'
  ),

  -- special "braço" originals (only usinado)
  special AS (
    SELECT id,
           COALESCE(part_number, 'PN' || id) AS base,
           COALESCE(description, '') AS description,
           category, client_ID, supplier_ID, cost
    FROM components_and_parts
    WHERE (lower(COALESCE(description,'')) LIKE '%braço%'
           OR lower(COALESCE(description,'')) LIKE '%pitman%')
      AND lower(COALESCE(part_number,'')) NOT LIKE '%-br-%'
      AND lower(COALESCE(part_number,'')) NOT LIKE '%-us-%'
  )

-- 1) Update non-special originals to BR-01 and set description to "... Bruto"
UPDATE components_and_parts
SET part_number = (SELECT base || '-BR-01' FROM origs o WHERE o.id = components_and_parts.id),
    description = (SELECT trim(description || ' Bruto') FROM origs o WHERE o.id = components_and_parts.id)
WHERE id IN (SELECT id FROM origs);

-- 2) Insert remaining Bruto variants (BR-02 .. BR-10)
INSERT INTO components_and_parts (part_number, description, category, client_ID, supplier_ID, cost)
SELECT o.base || printf('-BR-%02d', n), trim(o.description || ' Bruto'), o.category, o.client_ID, o.supplier_ID, o.cost
FROM origs o
CROSS JOIN nums_br
WHERE (o.base || printf('-BR-%02d', n)) NOT IN (SELECT part_number FROM components_and_parts);

-- 3) Insert Usinado variants (US-001 .. US-020) for non-special originals
INSERT INTO components_and_parts (part_number, description, category, client_ID, supplier_ID, cost)
SELECT o.base || printf('-US-%03d', n), trim(o.description || ' Usinado'), o.category, o.client_ID, o.supplier_ID, o.cost
FROM origs o
CROSS JOIN nums_us
WHERE (o.base || printf('-US-%03d', n)) NOT IN (SELECT part_number FROM components_and_parts);

-- 4) For special "braço" components: set original to US-001 with standardized description
UPDATE components_and_parts
SET part_number = (SELECT base || '-US-001' FROM special s WHERE s.id = components_and_parts.id),
    description = 'Braço pitman Usinado'
WHERE id IN (SELECT id FROM special);

-- 5) Insert remaining US-002 .. US-020 for special components
INSERT INTO components_and_parts (part_number, description, category, client_ID, supplier_ID, cost)
SELECT s.base || printf('-US-%03d', n), 'Braço pitman Usinado', s.category, s.client_ID, s.supplier_ID, s.cost
FROM special s
CROSS JOIN (SELECT n FROM nums_us WHERE n > 1) AS nums
WHERE (s.base || printf('-US-%03d', nums.n)) NOT IN (SELECT part_number FROM components_and_parts);

COMMIT;

-- End of script
