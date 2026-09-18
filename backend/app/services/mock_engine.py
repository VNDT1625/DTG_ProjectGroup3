"""
Mock Data Engine - Phục vụ kiểm thử tích hợp Frontend độc lập trong Sprint 1.
Lưu ý: Không sử dụng để đánh giá độ chính xác hay hiệu năng của mô hình AI-NIDS.
"""
import random
import time
from typing import List, Dict, Any

class MockEngine:
    @staticmethod
    def generate_predictions(total_rows: int = 100) -> Dict[str, Any]:
        t0 = time.time()
        predictions = []
        attack_count = 0
        
        for i in range(1, total_rows + 1):
            # Giả lập phân bố ~15% tấn công
            is_attack = random.random() < 0.15
            if is_attack:
                attack_count += 1
                score = round(random.uniform(0.72, 0.99), 3)
                level = "High"
                pred_str = "Attack"
                label = 1
            else:
                score = round(random.uniform(0.01, 0.28), 3)
                level = "Low" if score < 0.20 else "Medium"
                pred_str = "Normal"
                label = 0
                
            predictions.append({
                "row_id": i,
                "predicted_label": label,
                "prediction": pred_str,
                "risk_score": score,
                "risk_level": level,
                "ground_truth_label": label if random.random() < 0.8 else 0
            })
            
        exec_time = round((time.time() - t0) * 1000, 2)
        normal_count = total_rows - attack_count
        
        return {
            "pure_inference_time_ms": round(exec_time * 0.4, 2),
            "total_execution_time_ms": exec_time,
            "summary": {
                "total_flows": total_rows,
                "normal_count": normal_count,
                "attack_count": attack_count,
                "attack_percentage": round((attack_count / total_rows) * 100, 2) if total_rows > 0 else 0.0
            },
            "predictions": predictions
        }
