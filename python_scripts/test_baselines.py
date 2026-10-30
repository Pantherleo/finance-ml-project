"""Synthetic tests of forecast dates, split isolation, parsing and metrics."""
import copy
from datetime import date,timedelta
from io import StringIO
import unittest
from baseline_forecast import read_prices,metrics,evaluate,evaluate_regime


class BaselineTests(unittest.TestCase):
    def setUp(self):
        self.rows = [{'date':date(2020,1,1)+timedelta(days=i),'High':float(i+3),'Low':float(i+1),'Close':float(i+2)} for i in range(40)]

    def test_origin_precedes_target_and_both_are_test(self):
        result,predictions = evaluate_regime(self.rows)
        self.assertEqual(result['test_forecast_pairs'],5)
        self.assertEqual(predictions[0]['origin_date'],self.rows[34]['date'].isoformat())
        self.assertEqual(predictions[0]['High_persistence'],self.rows[34]['High'])
        self.assertEqual(predictions[0]['High_actual'],self.rows[35]['High'])

    def test_future_target_cannot_change_earlier_prediction(self):
        result,original = evaluate_regime(self.rows)
        changed = copy.deepcopy(self.rows)
        changed[35]['High'] *= 1000
        perturbed_result,perturbed = evaluate_regime(changed)
        for model in ('persistence','current_close','train_mean'):
            self.assertEqual(original[0]['High_'+model],perturbed[0]['High_'+model])
        self.assertEqual(result['training_constants'],perturbed_result['training_constants'])

    def test_metrics_and_constant_target(self):
        self.assertEqual(metrics([1.,3.],[2.,2.]),{'mae':1.,'rmse':1.,'r2':0.})
        self.assertIsNone(metrics([1.,1.],[2.,2.])['r2'])

    def test_no_imputation_and_invalid_rows_reported(self):
        text='Date,Close,High,Low\n'+'\n'.join(f'{i:02d}-01-2020,2,3,1' for i in [1,2,3,4,5,6,7,8,9,20])+'\n21-01-2020,,3,1\n'
        rows,quality = read_prices(StringIO(text))
        self.assertEqual(len(rows),10)
        self.assertEqual(quality['max_calendar_gap_days'],11)
        self.assertEqual(quality['rejected_by_reason']['missing_or_nonnumeric_price'],1)

    def test_duplicate_dates_rejected(self):
        text='Date,Close,High,Low\n'+'\n'.join('01-01-2020,2,3,1' for _ in range(10))
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            read_prices(StringIO(text))

    def test_regime_overlap_rejected(self):
        with self.assertRaisesRegex(ValueError,'overlap'):
            evaluate(self.rows,{'A':[2007,2020],'B':[2020,None]})


if __name__=='__main__':
    unittest.main()
