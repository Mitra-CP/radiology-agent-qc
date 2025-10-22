from typing import Dict, Any, Optional
try:
    import pydicom  # type: ignore
except Exception:
    pydicom = None

def read_dicom_header(path: str) -> Dict[str, Any]:
    if pydicom is None:
        return {}
    ds = pydicom.dcmread(path, stop_before_pixels=True, force=True)
    out = {}
    for tag in ['StudyInstanceUID','SeriesInstanceUID','Modality','ProtocolName',
                'BodyPartExamined','SliceThickness','RepetitionTime','EchoTime',
                'ContrastBolusAgent','PatientSex','StudyDate','Manufacturer','ManufacturerModelName']:
        if hasattr(ds, tag):
            out[tag] = getattr(ds, tag)
    return out
