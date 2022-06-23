from typing import Dict, Any
from core.utils import model_update
from samples.models import Sample


# keyword only arguments
def sample_create(
    *,
    field_name: str
) -> Sample:
    sample = Sample()
    sample.full_clean()
    sample.save()

    return sample


def sample_update(*, sample: Sample, data: Dict[str, Any]) -> Sample:
    sample, has_updated = model_update(instance=sample, data=data)

    return sample


def sample_delete(*, sample: Sample):
    sample.delete()
