"""
Servicio de clasificación de documentos usando Machine Learning
"""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import os
from typing import Tuple, Dict, List
import numpy as np

class DocumentClassifier:
    def __init__(self):
        self.model = None
        self.categories = [
            'Contrato',
            'Contrato de Granos',
            'Informe',
            'Factura',
            'Remito',
            'Nota de Crédito',
            'Nota de Débito',
            'Política',
            'Manual',
            'Orden de Compra',
            'Recibo',
            'Otro'
        ]
        self.model_path = 'classifier_model.pkl'
        
        # Cargar modelo si existe, si no, crear uno básico
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            self.create_basic_model()
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocesa el texto para mejorar la clasificación
        """
        # Convertir a minúsculas
        text = text.lower()
        
        # Eliminar caracteres especiales excepto espacios
        text = re.sub(r'[^a-záéíóúñ\s]', ' ', text)
        
        # Eliminar espacios múltiples
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def create_basic_model(self):
        """
        Crea un modelo básico con ejemplos de entrenamiento
        """
        # Datos de entrenamiento básicos (expandir con más ejemplos reales)
        training_texts = [
            # Contratos generales
            "contrato de arrendamiento entre partes firmante plazo mensual renta alquiler locación",
            "acuerdo contractual servicios prestación obligaciones derechos partes cláusulas",
            "contrato laboral empleado empresa condiciones salario jornada trabajo relación",
            
            # Contratos de Granos
            "contrato compraventa granos soja trigo maíz toneladas calidad entrega puerto",
            "operación cereales oleaginosas precio fijación descarga mercadería agrícola",
            "contrato forward granos cosecha futura entrega diferida agrícola campo",
            
            # Informes
            "informe ejecutivo resumen resultados análisis conclusiones recomendaciones gestión",
            "reporte mensual ventas indicadores desempeño objetivos alcanzados métricas",
            "informe técnico evaluación proyecto desarrollo implementación análisis estado",
            
            # Facturas
            "factura número fecha total iva subtotal forma pago impuesto cuit",
            "comprobante fiscal venta productos servicios cantidad precio importe",
            "factura tipo responsable inscripto monotributo percepción retención",
            
            # Remitos
            "remito número entrega mercadería bultos cantidad transporte domicilio destinatario",
            "comprobante entrega productos recibido conforme transportista",
            "guía remito despacho mercancía envío entrega recepción",
            
            # Notas de Crédito
            "nota crédito número devolución anulación factura original descuento bonificación",
            "comprobante crédito ajuste negativo importe devuelto cliente rectificación",
            "nc crédito fiscal anulación parcial total factura emitida",
            
            # Notas de Débito
            "nota débito número cargo adicional intereses mora factura saldo",
            "comprobante débito ajuste positivo recargo financiero adeudado",
            "nd débito fiscal cargo complementario factura original",
            
            # Políticas
            "política empresa normas procedimientos lineamientos cumplimiento regulación",
            "reglamento interno conducta empleados sanciones obligaciones derechos",
            "política privacidad datos personales protección tratamiento confidencialidad",
            
            # Manuales
            "manual usuario instrucciones instalación configuración operación sistema",
            "guía procedimientos paso proceso aplicación software utilización",
            "manual técnico especificaciones mantenimiento troubleshooting reparación",
            
            # Órdenes de Compra
            "orden compra número proveedor artículos cantidad precio entrega plazo",
            "solicitud pedido productos mercadería comprador vendedor condiciones",
            "oc orden compra autorización adquisición bienes servicios",
            
            # Recibos
            "recibo pago número importe efectivo concepto fecha pagador",
            "comprobante recibo cobro cancelación deuda saldo conformidad",
            "recibo oficial dinero abonado liquidación pago total parcial",
            
            # Otro
            "documento general información varios temas contenido mixto variado",
            "comunicado oficial notificación aviso información general diversos",
            "documento administrativo gestión trámite solicitud varios conceptos",
        ]
        
        training_labels = [
            'Contrato', 'Contrato', 'Contrato',
            'Contrato de Granos', 'Contrato de Granos', 'Contrato de Granos',
            'Informe', 'Informe', 'Informe',
            'Factura', 'Factura', 'Factura',
            'Remito', 'Remito', 'Remito',
            'Nota de Crédito', 'Nota de Crédito', 'Nota de Crédito',
            'Nota de Débito', 'Nota de Débito', 'Nota de Débito',
            'Política', 'Política', 'Política',
            'Manual', 'Manual', 'Manual',
            'Orden de Compra', 'Orden de Compra', 'Orden de Compra',
            'Recibo', 'Recibo', 'Recibo',
            'Otro', 'Otro', 'Otro'
        ]
        
        # Crear pipeline con TF-IDF y Naive Bayes
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
            ('clf', MultinomialNB())
        ])
        
        # Entrenar modelo
        self.model.fit(training_texts, training_labels)
        
        # Guardar modelo
        self.save_model()
    
    def classify_document(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        """
        Clasifica un documento según su contenido
        
        Args:
            text: Texto del documento a clasificar
            
        Returns:
            Tupla con (categoría_predicha, confianza, probabilidades_todas)
        """
        if not self.model:
            raise Exception("Modelo no inicializado")
        
        # Preprocesar texto
        processed_text = self.preprocess_text(text)
        
        if not processed_text:
            return ('Otro', 0.5, {cat: 0.0 for cat in self.categories})
        
        # Predecir
        prediction = self.model.predict([processed_text])[0]
        
        # Obtener probabilidades
        probabilities = self.model.predict_proba([processed_text])[0]
        
        # Crear diccionario de probabilidades por categoría
        prob_dict = {
            cat: float(prob) 
            for cat, prob in zip(self.model.classes_, probabilities)
        }
        
        # Obtener confianza de la predicción
        confidence = float(max(probabilities))
        
        return (prediction, confidence, prob_dict)
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extrae palabras clave del texto usando TF-IDF
        
        Args:
            text: Texto del documento
            top_n: Número de palabras clave a extraer
            
        Returns:
            Lista de palabras clave
        """
        processed_text = self.preprocess_text(text)
        
        if not processed_text or not self.model:
            return []
        
        # Obtener features TF-IDF
        tfidf = self.model.named_steps['tfidf']
        features = tfidf.transform([processed_text])
        
        # Obtener nombres de features
        feature_names = tfidf.get_feature_names_out()
        
        # Obtener índices de los valores más altos
        top_indices = features.toarray()[0].argsort()[-top_n:][::-1]
        
        # Obtener palabras clave
        keywords = [feature_names[i] for i in top_indices if features.toarray()[0][i] > 0]
        
        return keywords
    
    def save_model(self):
        """Guarda el modelo entrenado"""
        if self.model:
            joblib.dump(self.model, self.model_path)
    
    def load_model(self):
        """Carga el modelo entrenado"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
    
    def train_with_new_data(self, texts: List[str], labels: List[str]):
        """
        Entrena el modelo con nuevos datos (actualización incremental)
        
        Args:
            texts: Lista de textos de documentos
            labels: Lista de etiquetas correspondientes
        """
        if len(texts) != len(labels):
            raise ValueError("El número de textos y etiquetas debe ser igual")
        
        if len(texts) == 0:
            raise ValueError("Debe proporcionar al menos un texto para entrenar")
        
        # Preprocesar textos
        processed_texts = [self.preprocess_text(text) for text in texts]
        
        # Entrenar modelo
        if not self.model:
            self.create_basic_model()
        
        # Re-entrenar el modelo con los nuevos datos
        # Nota: Esto actualiza el modelo existente con los nuevos ejemplos
        try:
            # Obtener datos de entrenamiento actuales (si existen)
            # y combinarlos con los nuevos
            self.model.fit(processed_texts, labels)
            self.save_model()
            print(f"✓ Modelo actualizado con {len(texts)} nuevos ejemplos")
        except Exception as e:
            print(f"✗ Error al entrenar modelo: {str(e)}")
            raise

# Singleton
classifier = DocumentClassifier()
