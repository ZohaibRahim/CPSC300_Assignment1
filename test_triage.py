import unittest
import random
from patient import Patient
from triage_logic import setup_triage_rng, triage_walkin_priority_assignment, TRIAGE_RNG_SEED

class TriageTest(unittest.TestCase):
    
    def test_priority_sequence_matches_model_output(self):
        """Tests if the fixed-seed RNG produces the exact priority sequence for data1's walk-in patients."""

        print("Running triage priority test...")

        # Expected priorities from the model solution for walk-in patients: [3, 1, 2]
        EXPECTED_PRIORITIES = [3, 1, 2]
        
        # Reset the Patient ID counter and RNG instance before the first run
        Patient.NEXT_ID = 28064212 
        setup_triage_rng() 
        
        actual_priorities = []
        
        # Simulate patient creation sequence from data1 (E, W, E, W, E, W, E)
        # Order is critical as it consumes both IDs and random numbers (for W patients)
        
        # P28064212 (E) - ID consumed
        Patient(18, 'E', 2) 
        
        # P28064213 (W) - ID consumed, consumes RNG 1
        p_28064213 = Patient(18, 'W', 3) 
        actual_priorities.append(triage_walkin_priority_assignment(p_28064213))
        
        # P28064214 (E) - ID consumed
        Patient(19, 'E', 28) 
        
        # P28064215 (W) - ID consumed, consumes RNG 2
        p_28064215 = Patient(20, 'W', 19)
        actual_priorities.append(triage_walkin_priority_assignment(p_28064215))
        
        # P28064216 (E) - ID consumed
        Patient(20, 'E', 36)
        
        # P28064217 (W) - ID consumed, consumes RNG 3
        p_28064217 = Patient(21, 'W', 1)
        actual_priorities.append(triage_walkin_priority_assignment(p_28064217))
        
        # P28064218 (E) - ID consumed
        Patient(24, 'E', 10)

        self.assertEqual(actual_priorities, EXPECTED_PRIORITIES, 
                         f"RNG failed to produce: {EXPECTED_PRIORITIES}. Got: {actual_priorities}")

        # Test for consistency: Rerun to ensure the same sequence is generated (verifies fixed seed)
        Patient.NEXT_ID = 28064212 
        setup_triage_rng() 
        
        second_run_priorities = []
        
        # Re-run patient creation and priority assignment (identical sequence)
        Patient(18, 'E', 2) 
        p_28064213 = Patient(18, 'W', 3) 
        second_run_priorities.append(triage_walkin_priority_assignment(p_28064213))
        
        Patient(19, 'E', 28) 
        p_28064215 = Patient(20, 'W', 19)
        second_run_priorities.append(triage_walkin_priority_assignment(p_28064215))
        
        Patient(20, 'E', 36)
        p_28064217 = Patient(21, 'W', 1)
        second_run_priorities.append(triage_walkin_priority_assignment(p_28064217))
        
        Patient(24, 'E', 10)

        self.assertEqual(second_run_priorities, EXPECTED_PRIORITIES, 
                         "Second run failed: RNG must produce the identical sequence.")


if __name__ == '__main__':
    # Required for unittest to run cleanly in environments like VS Code/Jupyter
    unittest.main(argv=['first-arg-is-ignored'], exit=False)