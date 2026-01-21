class ValueEmpID:
    def __init__(self,emp_id):
        if len(emp_id) < 3:
            raise ValueError("emp_id has to be grather than 3 caracteres")
        self.emp_id = emp_id.upper()