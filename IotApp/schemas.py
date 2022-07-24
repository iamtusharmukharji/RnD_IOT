from pydantic import BaseModel



class DeviceEnrollData(BaseModel):
    chip_id: str
    location: str
    description: str