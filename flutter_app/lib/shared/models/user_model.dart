import 'package:json_annotation/json_annotation.dart';

part 'user_model.g.dart';

@JsonSerializable()
class UserModel {
  final String id;
  final String email;
  final String role;
  final String? institutionId;
  final String? name;
  final String? avatar;
  final DateTime createdAt;
  final DateTime updatedAt;
  
  UserModel({
    required this.id,
    required this.email,
    required this.role,
    this.institutionId,
    this.name,
    this.avatar,
    required this.createdAt,
    required this.updatedAt,
  });
  
  factory UserModel.fromJson(Map<String, dynamic> json) => _$UserModelFromJson(json);
  Map<String, dynamic> toJson() => _$UserModelToJson(this);
}

@JsonSerializable()
class InstitutionModel {
  final String id;
  final String name;
  final String type;
  final String? planType;
  final String? status;
  final DateTime createdAt;
  
  InstitutionModel({
    required this.id,
    required this.name,
    required this.type,
    this.planType,
    this.status,
    required this.createdAt,
  });
  
  factory InstitutionModel.fromJson(Map<String, dynamic> json) => _$InstitutionModelFromJson(json);
  Map<String, dynamic> toJson() => _$InstitutionModelToJson(this);
}

@JsonSerializable()
class LearningProfileModel {
  final String studentId;
  final String goalDomain;
  final List<SkillModel> skills;
  final LearningPreferencesModel preferences;
  
  LearningProfileModel({
    required this.studentId,
    required this.goalDomain,
    required this.skills,
    required this.preferences,
  });
  
  factory LearningProfileModel.fromJson(Map<String, dynamic> json) => _$LearningProfileModelFromJson(json);
  Map<String, dynamic> toJson() => _$LearningProfileModelToJson(this);
}

@JsonSerializable()
class SkillModel {
  final String code;
  final String name;
  final double level;
  final double target;
  final double confidence;
  
  SkillModel({
    required this.code,
    required this.name,
    required this.level,
    required this.target,
    required this.confidence,
  });
  
  factory SkillModel.fromJson(Map<String, dynamic> json) => _$SkillModelFromJson(json);
  Map<String, dynamic> toJson() => _$SkillModelToJson(this);
}

@JsonSerializable()
class LearningPreferencesModel {
  final List<String> contentFormat;
  final String pace;
  final String language;
  final String? dialect;
  
  LearningPreferencesModel({
    required this.contentFormat,
    required this.pace,
    required this.language,
    this.dialect,
  });
  
  factory LearningPreferencesModel.fromJson(Map<String, dynamic> json) => _$LearningPreferencesModelFromJson(json);
  Map<String, dynamic> toJson() => _$LearningPreferencesModelToJson(this);
}

@JsonSerializable()
class ProgressModel {
  final String studentId;
  final double overallProgress;
  final List<SkillProgressModel> skillProgress;
  final int completedLessons;
  final int totalLessons;
  final DateTime lastUpdated;
  
  ProgressModel({
    required this.studentId,
    required this.overallProgress,
    required this.skillProgress,
    required this.completedLessons,
    required this.totalLessons,
    required this.lastUpdated,
  });
  
  factory ProgressModel.fromJson(Map<String, dynamic> json) => _$ProgressModelFromJson(json);
  Map<String, dynamic> toJson() => _$ProgressModelToJson(this);
}

@JsonSerializable()
class SkillProgressModel {
  final String skillCode;
  final String skillName;
  final double currentLevel;
  final double targetLevel;
  final int completedItems;
  final int totalItems;
  
  SkillProgressModel({
    required this.skillCode,
    required this.skillName,
    required this.currentLevel,
    required this.targetLevel,
    required this.completedItems,
    required this.totalItems,
  });
  
  factory SkillProgressModel.fromJson(Map<String, dynamic> json) => _$SkillProgressModelFromJson(json);
  Map<String, dynamic> toJson() => _$SkillProgressModelToJson(this);
}