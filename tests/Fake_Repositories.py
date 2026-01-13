class FakeSectorRepository:
    def __init__(self, sectors=None):
        self.sectors = sectors
    

    def repo_get_all_sectors(self):
        return 