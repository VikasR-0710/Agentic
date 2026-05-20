from case_analysis.services.snowflake_service import SnowflakeService

sf = SnowflakeService()

print("\n===== DATABASES =====")
for row in sf.execute_query("SHOW DATABASES"):
    print(row)

sf.close()