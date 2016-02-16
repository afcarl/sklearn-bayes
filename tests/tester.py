# -*- coding: utf-8 -*-
import unittest
import numpy as np
import warnings

from sklearn.utils.estimator_checks import check_estimator
from sklearn_bayes.rvm.fast_rvm import RegressionARD,ClassificationARD,RVR,RVC
from sklearn_bayes.logistic.bayesian_logistic import BayesianLogisticRegression
from sklearn_bayes.logistic.variational_logistic import VariationalLogisticRegression
from sklearn_bayes.linear.bayesian_regression import BayesianRegression
from sklearn_bayes.linear.variational_regression import VariationalLinearRegression
from sklearn_bayes.vrvm.vrvm import VariationalRegressionARD,VRVR
# ignore all warnings


ESTIMATORS  = [  RegressionARD, RVR, BayesianRegression, VariationalRegressionARD,
                 VRVR, VariationalLinearRegression, RVC, ClassificationARD,
                 BayesianLogisticRegression, VariationalLogisticRegression
              ]
                
REGRESSORS  = [  RegressionARD, BayesianRegression, VariationalRegressionARD,
                 VRVR, VariationalLinearRegression, RVR
              ]


class TestSupervised(unittest.TestCase):
    '''
    This class utilizes vast number of tests in sklearn package for 
    regression / classification, ensures that all models in sklearn_bayes follow
    sklearn API
    '''
    
    def test_sklearn_estimator(self):
        '''
        Tests each regression / classification model by invoking extensive
        sklearn test suite
        '''        
        for estimator in ESTIMATORS:
            check_estimator(estimator)
            
    
    def test_predict_dist(self):
        '''
        Tests the only public method in implemented classes that is not
        tested in sklearn test suits ["predict_dist" - defined only for regressors]
        '''
        # small example witth  perfect multicollinearity
        X  = np.array([ [ 0.1,  -0.1,  -0.2,   0.02],
                        [ 0.3,  -0.3,  -0.6,   0.06],
                        [ 0.4,  -0.4,  -0.8,   0.08],
                        [ 0.5,  -0.5,  -1.,    0.1 ]])

        y  = np.array([ 2,  6,  8,  10.])
        
        for r_model in REGRESSORS:
            model = r_model()
            # expect warnings for near perfect fit
            model.fit(X,y)
            yh, vh = model.predict_dist(X)
            
            # test shapes of mean and std for predictive distribution
            self.assertEqual( yh.shape[0],vh.shape[0])
            
            # test that all elements of predicted standard deviation are non-negative
            self.assertEqual( np.sum( yh < 0), 0)
            
            # test that point prediction is not far from desired
            # (Note!!! It should not be exactly equal, since all of these models 
            # have regularization, )
            np.testing.assert_allclose(yh,y,atol = 0.5)
            
            # test that 'predict' and 'predict_dist' return the same point estimate
            # ( Note! in RVR & VRVR these are calculated differently)
            np.testing.assert_allclose( model.predict(X), yh)

    
if __name__ == '__main__':
    unittest.main()
