import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple

class ModelEvaluator:
    """Class for evaluating IoT botnet detection models"""
    
    def __init__(self):
        self.metrics = {}
        
    def evaluate_model(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Evaluate model performance using various metrics
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            
        Returns:
            Dictionary containing evaluation metrics
        """
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted')
        }
        
        self.metrics = metrics
        return metrics
    
    def plot_confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray,
                            labels: List[str] = None) -> None:
        """
        Plot confusion matrix
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            labels: Label names
        """
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        if labels:
            plt.xticks(np.arange(len(labels)) + 0.5, labels, rotation=45)
            plt.yticks(np.arange(len(labels)) + 0.5, labels, rotation=0)
        plt.tight_layout()
        
    def get_performance_summary(self) -> str:
        """
        Get a text summary of model performance
        
        Returns:
            String containing performance summary
        """
        if not self.metrics:
            return "No evaluation metrics available. Run evaluate_model first."
            
        summary = "Model Performance Summary:\n"
        summary += f"Accuracy: {self.metrics['accuracy']:.4f}\n"
        summary += f"Precision: {self.metrics['precision']:.4f}\n"
        summary += f"Recall: {self.metrics['recall']:.4f}\n"
        summary += f"F1 Score: {self.metrics['f1']:.4f}\n"
        
        return summary 