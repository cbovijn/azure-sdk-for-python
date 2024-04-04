# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import datetime
import os

from azure.core.credentials import AzureKeyCredential
from azure.healthinsights.radiologyinsights import RadiologyInsightsClient
from azure.healthinsights.radiologyinsights import models

"""
FILE: sample_laterality_discrepancy_inference.py

DESCRIPTION:
The sample_laterality_discrepancy_inference.py module processes a sample radiology document with the Radiology Insights service.
It will initialize a RadiologyInsightsClient, build a Radiology Insights request with the sample document,
submit it to the client, RadiologyInsightsClient, build a Radiology Insights job request with the sample document,
submit it to the client and display the Laterality Mismatch indication and descripancy type extracted by the Radiology Insights service.     


USAGE:
   
"""


class HealthInsightsSyncSamples:
    def radiology_insights_sync(self) -> None:
        KEY = os.environ["AZURE_HEALTH_INSIGHTS_API_KEY"]
        ENDPOINT = os.environ["AZURE_HEALTH_INSIGHTS_ENDPOINT"]

        radiology_insights_client = RadiologyInsightsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))
        
        doc_content1 = """Exam:   US LT BREAST TARGETED
        Technique:  Targeted imaging of the  right breast  is performed.
        Findings:
        Targeted imaging of the left breast is performed from the 6:00 to the 9:00 position.
        At the 6:00 position, 5 cm from the nipple, there is a 3 x 2 x 4 mm minimally hypoechoic mass with a peripheral calcification. 
        This may correspond to the mammographic finding. No other cystic or solid masses visualized."""
        
        # Create ordered procedure
        procedure_coding = models.Coding(
            system="Https://loinc.org",
            code="26688-1",
            display="US BREAST - LEFT LIMITED",
        )
        procedure_code = models.CodeableConcept(coding=[procedure_coding])
        ordered_procedure = models.OrderedProcedure(description="US BREAST - LEFT LIMITED", code=procedure_code)
        # Create encounter
        start = datetime.datetime(2021, 8, 28, 0, 0, 0, 0)
        end = datetime.datetime(2021, 8, 28, 0, 0, 0, 0)
        encounter = models.Encounter(
            id="encounter2",
            class_property=models.EncounterClass.IN_PATIENT,
            period=models.TimePeriod(start=start, end=end),
        )
        # Create patient info
        birth_date = datetime.date(1959, 11, 11)
        patient_info = models.PatientDetails(sex=models.PatientSex.FEMALE, birth_date=birth_date)
        # Create author
        author = models.DocumentAuthor(id="author2", full_name="authorName2")

        create_date_time = datetime.datetime(2024, 2, 19, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)
        patient_document1 = models.PatientDocument(
            type=models.DocumentType.NOTE,
            clinical_type=models.ClinicalDocumentType.RADIOLOGY_REPORT,
            id="doc2",
            content=models.DocumentContent(source_type=models.DocumentContentSourceType.INLINE, value=doc_content1),
            created_date_time=create_date_time,
            specialty_type=models.SpecialtyType.RADIOLOGY,
            administrative_metadata=models.DocumentAdministrativeMetadata(
                ordered_procedures=[ordered_procedure], encounter_id="encounter2"
            ),
            authors=[author],
            language="en",
        )

        # Construct patient
        patient1 = models.PatientRecord(
            id="patient_id2",
            info=patient_info,
            encounters=[encounter],
            patient_documents=[patient_document1],
        )

        # Create a configuration
        configuration = models.RadiologyInsightsModelConfiguration(verbose=False, include_evidence=True, locale="en-US")

        # Construct the request with the patient and configuration
        radiology_insights_data = models.RadiologyInsightsData(patients=[patient1], configuration=configuration)

        # Health Insights Radiology Insights
        try:
            poller = radiology_insights_client.begin_infer_radiology_insights(
                radiology_insights_data,
            )
            radiology_insights_result = poller.result()
            self.display_laterality_discrepancy(radiology_insights_result)
        except Exception as ex:
            print(str(ex))
            return

    def display_laterality_discrepancy(self, radiology_insights_result):
        for patient_result in radiology_insights_result.patient_results:
            for ri_inference in patient_result.inferences:
                if ri_inference.kind == models.RadiologyInsightsInferenceType.LATERALITY_DISCREPANCY:
                    print(f"{ri_inference.kind.name} Inference Found")
                    indication = ri_inference.laterality_indication 
                    for code in indication.coding:
                         print(f"{ri_inference.kind.name}: Laterality Indication: {code.system} {code.code} {code.display}")
                    print(f"{ri_inference.kind.name}: Discrepancy Type: {ri_inference.discrepancy_type}")
        
def main():
    sample = HealthInsightsSyncSamples()
    sample.radiology_insights_sync()


if __name__ == "__main__":
    main()
