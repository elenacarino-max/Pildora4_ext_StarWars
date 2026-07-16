import unittest

from core.code_validator import validate_chamber, validate_mission_submission


class CodeValidatorTests(unittest.TestCase):
    def test_accepts_experiment(self):
        result = validate_chamber("experiment", 'mlflow.set_experiment("Biblioteca_Jedi_Digits")')
        self.assertTrue(result.valid)

    def test_rejects_metric_as_parameter(self):
        result = validate_chamber("metrics", 'mlflow.log_param("accuracy", accuracy)')
        self.assertFalse(result.valid)
        self.assertIn("métrica", result.message)

    def test_rejects_arbitrary_execution(self):
        result = validate_chamber("parameters", 'open("secreto.txt").read()')
        self.assertFalse(result.valid)
        self.assertIn("autorizada", result.message)

    def test_requires_two_artifacts(self):
        code = '''with mlflow.start_run(run_name="Mision_Tatooine"):
    mlflow.log_params(parametros)
    mlflow.log_metrics(metricas)
    mlflow.log_artifact("matriz.png")
    mlflow.sklearn.log_model(sk_model=modelo, artifact_path="modelo_digits")'''
        result = validate_mission_submission(code)
        self.assertFalse(result.valid)
        self.assertIn("dos artefactos", result.message)


if __name__ == "__main__":
    unittest.main()
