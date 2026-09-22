
# İLAYDA BALAL - 03.12.2025

"""
Özel NLP ve ML Algoritmaları Modülü
"""

import numpy as np
import re
from collections import Counter, defaultdict
from math import log, sqrt, exp
from abc import ABC, abstractmethod


class TurkceMetinTemizleyici:
    """Türkçe metin ön işleme sınıfı"""
    
    def __init__(self):
        self.durak_kelimeler = {
            've', 'veya', 'ile', 'için', 've', 'bir', 'bu', 'şu', 'o',
            'de', 'da', 'den', 'dan', 'ki', 'mi', 'mu', 'mü', 'gibi',
            'daha', 'çok', 'az', 'var', 'yok', 'ama', 'fakat', 'ancak',
            'ya', 'hem', 'ne', 'nasıl', 'neden', 'niçin', 'nerede'
        }
    
    def temizle(self, metin):
        if not isinstance(metin, str):
            return ""
        
        metin = metin.lower()
        
        metin = re.sub(r'http\S+|www\S+', '', metin)
        
        metin = re.sub(r'\S+@\S+', '', metin)
        
        metin = re.sub(r'[^\w\sçğıöşüÇĞİÖŞÜ]', ' ', metin)
        
        metin = re.sub(r'\s+', ' ', metin)
        
        return metin.strip()
    
    def tokenize(self, metin):
        metin = self.temizle(metin)
        kelimeler = metin.split()
        return [k for k in kelimeler if len(k) > 2]  
    
    def durak_kelime_cikar(self, kelimeler):
        return [k for k in kelimeler if k not in self.durak_kelimeler]


class TFIDFVectorizer:

    def __init__(self, max_features=10000, ngram_range=(1, 2), min_df=2, max_df=0.8):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.min_df = min_df
        self.max_df = max_df
        
        self.vocabulary = {}
        self.idf_values = {}
        self.feature_names = []
        self.temizleyici = TurkceMetinTemizleyici()
    
    def _kelime_frekansi_hesapla(self, kelimeler):
        toplam = len(kelimeler)
        if toplam == 0:
            return {}
        
        frekans = Counter(kelimeler)
        return {kelime: sayı / toplam for kelime, sayı in frekans.items()}
    
    def _ngram_olustur(self, kelimeler, n):
        ngrams = []
        for i in range(len(kelimeler) - n + 1):
            ngram = ' '.join(kelimeler[i:i+n])
            ngrams.append(ngram)
        return ngrams
    
    def _dokuman_frekansi_hesapla(self, dokuman_listesi):
        df = Counter()
        for dokuman in dokuman_listesi:
            unique_terms = set(dokuman)
            df.update(unique_terms)
        return df
    
    def fit(self, metinler):
        n_dokumanlar = len(metinler)
        
        tum_terimler = []
        dokuman_terimleri = []
        
        for metin in metinler:
            kelimeler = self.temizleyici.tokenize(metin)
            
            terimler = []
            for n in range(self.ngram_range[0], self.ngram_range[1] + 1):
                if n == 1:
                    terimler.extend(kelimeler)
                else:
                    terimler.extend(self._ngram_olustur(kelimeler, n))
            
            tum_terimler.extend(terimler)
            dokuman_terimleri.append(terimler)
        
        df = self._dokuman_frekansi_hesapla(dokuman_terimleri)
        
        min_doc_count = max(1, self.min_df if isinstance(self.min_df, int) else int(self.min_df * n_dokumanlar))
        max_doc_count = self.max_df if isinstance(self.max_df, int) else int(self.max_df * n_dokumanlar)
        
        filtreli_terimler = [
            terim for terim, sayı in df.items()
            if min_doc_count <= sayı <= max_doc_count
        ]
        
        terim_frekanslari = Counter(tum_terimler)
        en_populer = [terim for terim, _ in terim_frekanslari.most_common(self.max_features)
                      if terim in filtreli_terimler]
        
        self.vocabulary = {terim: idx for idx, terim in enumerate(en_populer)}
        self.feature_names = en_populer
        
        for terim in en_populer:
            doc_count = df.get(terim, 0)
            self.idf_values[terim] = log((n_dokumanlar + 1) / (doc_count + 1)) + 1
        
        return self
    
    def transform(self, metinler):
        n_features = len(self.vocabulary)
        n_samples = len(metinler)
        
        tfidf_matrix = np.zeros((n_samples, n_features))
        
        for doc_idx, metin in enumerate(metinler):
            kelimeler = self.temizleyici.tokenize(metin)
            
            terimler = []
            for n in range(self.ngram_range[0], self.ngram_range[1] + 1):
                if n == 1:
                    terimler.extend(kelimeler)
                else:
                    terimler.extend(self._ngram_olustur(kelimeler, n))
            
            tf = self._kelime_frekansi_hesapla(terimler)
            
            for terim, tf_value in tf.items():
                if terim in self.vocabulary:
                    idx = self.vocabulary[terim]
                    idf_value = self.idf_values[terim]
                    tfidf_matrix[doc_idx, idx] = tf_value * idf_value
            
            norm = np.linalg.norm(tfidf_matrix[doc_idx])
            if norm > 0:
                tfidf_matrix[doc_idx] /= norm
        
        return tfidf_matrix
    
    def fit_transform(self, metinler):
        self.fit(metinler)
        return self.transform(metinler)
    
    def get_feature_names(self):
        return self.feature_names


class BaseClassifier(ABC):
    
    @abstractmethod
    def fit(self, X, y):
        """
        Modeli eğit
        
        Args:
            X: Özellik matrisi (n_samples, n_features)
            y: Hedef değişken (n_samples,)
        
        Returns:
            self: Eğitilmiş model
        """
        pass
    
    @abstractmethod
    def predict(self, X):
        """
        Sınıf tahminleri yap
        
        Args:
            X: Özellik matrisi (n_samples, n_features)
        
        Returns:
            y_pred: Tahminler (n_samples,)
        """
        pass
    
    @abstractmethod
    def predict_proba(self, X):
        """
        Olasılık tahminleri yap
        
        Args:
            X: Özellik matrisi (n_samples, n_features)
        
        Returns:
            proba: Olasılık matrisi (n_samples, n_classes)
        """
        pass
    
    @property
    def classes(self):
        if hasattr(self, 'classes_'):
            return self.classes_
        if hasattr(self, '_classes'):
            return self._classes
        raise AttributeError("Model henüz eğitilmedi! fit() metodunu çağırın.")


class MultinomialNaiveBayes(BaseClassifier):

    def __init__(self, alpha=1.0):
        self.alpha = alpha  
        self.classes_ = None
        self.class_log_priors = {}
        self.feature_log_probs = {}
    
    def fit(self, X, y):
        n_samples, n_features = X.shape
        
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)
        
        for c in self.classes_:
            X_c = X[y == c]
            
            self.class_log_priors[c] = log(len(X_c) / n_samples)
            
            feature_counts = X_c.sum(axis=0) + self.alpha
            total_count = feature_counts.sum()
            
            self.feature_log_probs[c] = np.log(feature_counts / total_count)
        
        return self
    
    def predict_proba(self, X):
        n_samples = X.shape[0]
        
        classes = self.classes_ if hasattr(self, 'classes_') else self.classes
        n_classes = len(classes)
        
        log_probs = np.zeros((n_samples, n_classes))
        
        for idx, c in enumerate(classes):
            log_prob = self.class_log_priors[c]
            log_prob += (X * self.feature_log_probs[c]).sum(axis=1)
            log_probs[:, idx] = log_prob
        
        max_log_prob = log_probs.max(axis=1, keepdims=True)
        exp_probs = np.exp(log_probs - max_log_prob)
        probs = exp_probs / exp_probs.sum(axis=1, keepdims=True)
        
        return probs
    
    def predict(self, X):
        probs = self.predict_proba(X)
        classes = self.classes_ if hasattr(self, 'classes_') else self.classes
        return classes[np.argmax(probs, axis=1)]


class LogisticRegressionManuel(BaseClassifier):

    def __init__(self, learning_rate=0.01, n_iterations=1000, reg_lambda=0.1):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.reg_lambda = reg_lambda  # L2 regularization
        self.weights = None
        self.bias = None
        self.classes_ = None
    
    def _softmax(self, z):
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)
    
    def _one_hot_encode(self, y):
        n_samples = len(y)
        n_classes = len(self.classes_)
        
        y_encoded = np.zeros((n_samples, n_classes))
        for idx, c in enumerate(self.classes_):
            y_encoded[y == c, idx] = 1
        
        return y_encoded
    
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)
        
        y_encoded = self._one_hot_encode(y)
        
        self.weights = np.random.randn(n_features, n_classes) * 0.01
        self.bias = np.zeros(n_classes)
        
        for iteration in range(self.n_iterations):
            z = np.dot(X, self.weights) + self.bias
            y_pred = self._softmax(z)
            
            error = y_pred - y_encoded
            
            dw = (1 / n_samples) * np.dot(X.T, error) + (self.reg_lambda / n_samples) * self.weights
            db = (1 / n_samples) * np.sum(error, axis=0)
            
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
            
            if iteration % 100 == 0:
                loss = self._compute_loss(X, y_encoded)
                print(f"      Iteration {iteration}, Loss: {loss:.4f}")
        
        return self
    
    def _compute_loss(self, X, y_encoded):
        n_samples = X.shape[0]
        z = np.dot(X, self.weights) + self.bias
        y_pred = self._softmax(z)
        
        loss = -np.sum(y_encoded * np.log(y_pred + 1e-10)) / n_samples
        
        loss += (self.reg_lambda / (2 * n_samples)) * np.sum(self.weights ** 2)
        
        return loss
    
    def predict_proba(self, X):
        z = np.dot(X, self.weights) + self.bias
        return self._softmax(z)
    
    def predict(self, X):
        probs = self.predict_proba(X)
        classes = self.classes_ if hasattr(self, 'classes_') else self.classes
        return classes[np.argmax(probs, axis=1)]


class ModelDegerlendirici:
    
    @staticmethod
    def accuracy(y_true, y_pred):
        return np.mean(y_true == y_pred)
    
    @staticmethod
    def confusion_matrix(y_true, y_pred, classes):
        n_classes = len(classes)
        matrix = np.zeros((n_classes, n_classes), dtype=int)
        
        class_to_idx = {c: i for i, c in enumerate(classes)}
        
        for true, pred in zip(y_true, y_pred):
            i = class_to_idx[true]
            j = class_to_idx[pred]
            matrix[i, j] += 1
        
        return matrix
    
    @staticmethod
    def classification_report(y_true, y_pred, classes):
        results = {}
        
        for c in classes:
            tp = np.sum((y_true == c) & (y_pred == c))
            fp = np.sum((y_true != c) & (y_pred == c))
            fn = np.sum((y_true == c) & (y_pred != c))
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            support = np.sum(y_true == c)
            
            results[c] = {
                'precision': precision,
                'recall': recall,
                'f1-score': f1,
                'support': support
            }
        
        macro_precision = np.mean([r['precision'] for r in results.values()])
        macro_recall = np.mean([r['recall'] for r in results.values()])
        macro_f1 = np.mean([r['f1-score'] for r in results.values()])
        
        results['macro avg'] = {
            'precision': macro_precision,
            'recall': macro_recall,
            'f1-score': macro_f1,
            'support': len(y_true)
        }
        
        total_support = len(y_true)
        weighted_precision = sum(r['precision'] * r['support'] for r in results.values() if isinstance(r, dict) and 'support' in r) / total_support
        weighted_recall = sum(r['recall'] * r['support'] for r in results.values() if isinstance(r, dict) and 'support' in r) / total_support
        weighted_f1 = sum(r['f1-score'] * r['support'] for r in results.values() if isinstance(r, dict) and 'support' in r) / total_support
        
        results['weighted avg'] = {
            'precision': weighted_precision,
            'recall': weighted_recall,
            'f1-score': weighted_f1,
            'support': total_support
        }
        
        results['accuracy'] = ModelDegerlendirici.accuracy(y_true, y_pred)
        
        return results


class CrossValidator:
    
    @staticmethod
    def kfold_split(X, y, n_splits=5):
        n_samples = len(X)
        indices = np.arange(n_samples)
        np.random.shuffle(indices)
        
        fold_sizes = np.full(n_splits, n_samples // n_splits, dtype=int)
        fold_sizes[:n_samples % n_splits] += 1
        
        current = 0
        for fold_size in fold_sizes:
            start, stop = current, current + fold_size
            test_indices = indices[start:stop]
            train_indices = np.concatenate([indices[:start], indices[stop:]])
            
            yield train_indices, test_indices
            current = stop
    
    @staticmethod
    def cross_val_score(model, X, y, cv=5):
        scores = []
        
        for train_idx, test_idx in CrossValidator.kfold_split(X, y, n_splits=cv):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            accuracy = ModelDegerlendirici.accuracy(y_test, y_pred)
            scores.append(accuracy)
        
        return np.array(scores)


# Test
if __name__ == "__main__":
    print("=" * 80)
    print(" NLP ve ML Algoritmaları Test ".center(80))
    print("=" * 80)
    
    test_metinler = [
        "Futbol maçında gol atıldı takım kazandı",
        "Basketbol finalinde heyecan vardı",
        "Dolar kuru yükseldi ekonomi etkilendi",
        "Borsa düştü yatırımcılar endişeli"
    ]
    
    test_etiketler = np.array(['spor', 'spor', 'ekonomi', 'ekonomi'])
    
    print("\n1. TF-IDF Vectorizer Test")
    print("-" * 80)
    vectorizer = TFIDFVectorizer(max_features=50, min_df=1)
    X = vectorizer.fit_transform(test_metinler)
    print(f"Matrix shape: {X.shape}")
    print(f"Vocabulary size: {len(vectorizer.vocabulary)}")
    
    print("\n2. Naive Bayes Test")
    print("-" * 80)
    nb = MultinomialNaiveBayes()
    nb.fit(X, test_etiketler)
    predictions = nb.predict(X)
    print(f"Predictions: {predictions}")
    print(f"Accuracy: {ModelDegerlendirici.accuracy(test_etiketler, predictions):.2f}")
    
    print("\n" + "=" * 80)
    print("Tüm testler başarılı!")