from odoo import fields, models

class AllamniStudent(models.Model):
    _name="allamni.student"
    _description="Allamni Student"
    name=fields.Char(required=True)
    email=fields.Char()
    learning_level=fields.Float(default=0)
    roadmap_progress=fields.Float(default=0)
    engagement_score=fields.Float(default=0)
    risk_level=fields.Selection([("low","Low"),("medium","Medium"),("high","High")],default="low")
    external_student_id=fields.Char(index=True)
