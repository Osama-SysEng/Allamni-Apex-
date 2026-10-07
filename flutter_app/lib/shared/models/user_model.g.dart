// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

UserModel _$UserModelFromJson(Map<String, dynamic> json) => UserModel(
      id: json['id'] as String,
      email: json['email'] as String,
      role: json['role'] as String,
      institutionId: json['institution_id'] as String?,
      name: json['name'] as String?,
      avatar: json['avatar'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );

Map<String, dynamic> _$UserModelToJson(UserModel instance) => <String, dynamic>{
      'id': instance.id,
      'email': instance.email,
      'role': instance.role,
      'institution_id': instance.institutionId,
      'name': instance.name,
      'avatar': instance.avatar,
      'created_at': instance.createdAt.toIso8601String(),
      'updated_at': instance.updatedAt.toIso8601String(),
    };

InstitutionModel _$InstitutionModelFromJson(Map<String, dynamic> json) =>
    InstitutionModel(
      id: json['id'] as String,
      name: json['name'] as String,
      type: json['type'] as String,
      planType: json['plan_type'] as String?,
      status: json['status'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$InstitutionModelToJson(InstitutionModel instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'type': instance.type,
      'plan_type': instance.planType,
      'status': instance.status,
      'created_at': instance.createdAt.toIso8601String(),
    };

LearningProfileModel _$LearningProfileModelFromJson(Map<String, dynamic> json) =>
    LearningProfileModel(
      studentId: json['student_id'] as String,
      goalDomain: json['goal_domain'] as String,
      skills: (json['skills'] as List<dynamic>)
          .map((e) => SkillModel.fromJson(e as Map<String, dynamic>))
          .toList(),
      preferences: LearningPreferencesModel.fromJson(
          json['preferences'] as Map<String, dynamic>),
    );

Map<String, dynamic> _$LearningProfileModelToJson(
        LearningProfileModel instance) =>
    <String, dynamic>{
      'student_id': instance.studentId,
      'goal_domain': instance.goalDomain,
      'skills': instance.skills.map((e) => e.toJson()).toList(),
      'preferences': instance.preferences.toJson(),
    };

SkillModel _$SkillModelFromJson(Map<String, dynamic> json) => SkillModel(
      code: json['code'] as String,
      name: json['name'] as String,
      level: (json['level'] as num).toDouble(),
      target: (json['target'] as num).toDouble(),
      confidence: (json['confidence'] as num).toDouble(),
    );

Map<String, dynamic> _$SkillModelToJson(SkillModel instance) => <String, dynamic>{
      'code': instance.code,
      'name': instance.name,
      'level': instance.level,
      'target': instance.target,
      'confidence': instance.confidence,
    };

LearningPreferencesModel _$LearningPreferencesModelFromJson(
        Map<String, dynamic> json) =>
    LearningPreferencesModel(
      contentFormat: (json['content_format'] as List<dynamic>).cast<String>(),
      pace: json['pace'] as String,
      language: json['language'] as String,
      dialect: json['dialect'] as String?,
    );

Map<String, dynamic> _$LearningPreferencesModelToJson(
        LearningPreferencesModel instance) =>
    <String, dynamic>{
      'content_format': instance.contentFormat,
      'pace': instance.pace,
      'language': instance.language,
      'dialect': instance.dialect,
    };

ProgressModel _$ProgressModelFromJson(Map<String, dynamic> json) => ProgressModel(
      studentId: json['student_id'] as String,
      overallProgress: (json['overall_progress'] as num).toDouble(),
      skillProgress: (json['skill_progress'] as List<dynamic>)
          .map((e) => SkillProgressModel.fromJson(e as Map<String, dynamic>))
          .toList(),
      completedLessons: json['completed_lessons'] as int,
      totalLessons: json['total_lessons'] as int,
      lastUpdated: DateTime.parse(json['last_updated'] as String),
    );

Map<String, dynamic> _$ProgressModelToJson(ProgressModel instance) =>
    <String, dynamic>{
      'student_id': instance.studentId,
      'overall_progress': instance.overallProgress,
      'skill_progress': instance.skillProgress.map((e) => e.toJson()).toList(),
      'completed_lessons': instance.completedLessons,
      'total_lessons': instance.totalLessons,
      'last_updated': instance.lastUpdated.toIso8601String(),
    };

SkillProgressModel _$SkillProgressModelFromJson(Map<String, dynamic> json) =>
    SkillProgressModel(
      skillCode: json['skill_code'] as String,
      skillName: json['skill_name'] as String,
      currentLevel: (json['current_level'] as num).toDouble(),
      targetLevel: (json['target_level'] as num).toDouble(),
      completedItems: json['completed_items'] as int,
      totalItems: json['total_items'] as int,
    );

Map<String, dynamic> _$SkillProgressModelToJson(SkillProgressModel instance) =>
    <String, dynamic>{
      'skill_code': instance.skillCode,
      'skill_name': instance.skillName,
      'current_level': instance.currentLevel,
      'target_level': instance.targetLevel,
      'completed_items': instance.completedItems,
      'total_items': instance.totalItems,
    };