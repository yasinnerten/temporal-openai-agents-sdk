def validate_all_skills():
    """Validate all skills in the skills directory."""
    print("🔍 Validating Agent Skills...")
    
    skills_dir = Path("skills")
    if not skills_dir.exists():
        print("❌ Skills directory not found")
        return
    
    valid_count = 0
    error_count = 0
    
    try:
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    valid, message, data = validate_skill(skill_file)
                    if valid:
                        print(f"✅ {data[0]}: {data[1]}")
                        valid_count += 1
                    else:
                        print(f"❌ {message}")
                        error_count += 1
    except Exception as e:
        print(f"❌ Error during validation: {e}")
    
    print(f"\n📊 Summary:")
    print(f"  Valid: {valid_count}")
    print(f"  Errors: {error_count}")