import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Baysian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        # Implement model selection based on BIC scores
        """
        BIC = −2 log L + p log N
        where L is the likelihood of the fitted model, p is the number of parameters,
        and N is the number of data points. The term −2 log L decreases with increasing model
        complexity (more parameters), whereas the penalties 2p or p log N increase with increasing complexity.
        The BIC applies a larger penalty whenN>e2 =7.4.
        """
        best_model = None
        best_bicscore = float('+inf')

        for num_states in range(self.min_n_components, self.max_n_components + 1):

            try:
                model = self.base_model(num_states)
                num_features = model.n_features
                logL = model.score(self.X, self.lengths)
                p = (num_states ** 2) + (2 * num_states * num_features)  - 1
                bic = -2 * logL + p * np.log(num_features)
                if bic < best_bicscore:
                    best_bicscore = bic
                    best_model = model
            except:
                continue

        return best_model




class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        # warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        # Implement model selection based on DIC scores

        best_dic_score = float('-inf')
        best_model = None
        for num_state in range(self.min_n_components, self.max_n_components + 1):

            try:
                model = self.base_model(num_state)
                # the likelihood of the data
                logL = model.score(self.X, self.lengths) #log likelihood
            except:
                continue

            sum_anti_logL = 0
            m = 0
            # the average of anti-likelihood terms
            for word in self.hwords.keys():
                x, length = self.hwords[word]
                if word != self.this_word:
                    try:
                        sum_anti_logL += model.score(x, length)
                        m += 1
                    except:
                        continue
            if m > 0:
                dic_score = logL - 1 / (m-1) * sum_anti_logL
            else:
                dic_score = 0

            if dic_score > best_dic_score:
                best_dic_score = dic_score
                best_model = model

        return best_model


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        # Implement model selection using CV

        # best_score = float('-inf')
        #n_splits = min(3, len(self.lengths))
        logL_ary = []
        score_model_ary = []
        split_method = KFold(n_splits = 3, shuffle = False, random_state = None)
        for num_states in range(self.min_n_components, self.max_n_components + 1):
            try:
                if len(self.sequences) > 2:
                    for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                        # In order to run hmmlearn training using the X,lengths tuples on the new folds,
                        # subsets must be combined based on the indices given for the folds.
                        self.X, self.lengths = combine_sequences(cv_train_idx, self.sequences)
                        X_test, test_lengths = combine_sequences(cv_test_idx, self.sequences)
                        model = self.base_model(num_states)
                        logL_score = model.score(X_test, test_lengths)
                else:
                    model = self.base_model(num_states)
                    logL_score = model.score(self.X, self.lengths)  # log likelihood
                logL_ary.append(logL_score)
                average_logL = np.mean(logL_ary)
                score_model_ary.append(tuple([average_logL, model]))
            except:
                pass
        # print("________________")
        # print(score_model_ary)
        if len(score_model_ary) > 0:
            score_mode = max(score_model_ary, key=lambda x: x[0])
            return score_mode[1]
        else:
            return None



