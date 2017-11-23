GrippeNet.fr Launch Procedure
================

Needs:
 - epipop webserver access
 - epipopDB server access
 - working copy for R GrippeNet Analysis project

Paths:
 - [epipop] = Path to working copy of GrippeNet website on epipop web server
 - [REpipop] = Path to working copy of GrippeNet Analysis (R epipop repository)
 -  ./ scripts in the same directory as this file

Surveys must be unpublished an republished to create new tables empty for the season

*CAUTION* Database actions MUST be done using epiwork user (Use pgadmin on epipopDB server using Xming)

Before Launch
====
 - Unpublish weekly & intake survey, modify if necessary and republish (using "Full edition" interface !)
    * Caution for weekly: need to drop pollster_health_view manually using DROP CASCADE
 - Create view for last season pointing to backup table containing last season data
	* SQL template in ./pollster_health_views_year.sql
	* Replace tags {year} by last season year
	* Replace {table_weekly_archive}, {table_intake_archive} by backup table with the last season's data created when surveys were unpublished
	* Run the script on epiwork DBlo
 - Modify HISTORY_TABLES to add last season entry in [epipop]/local_settings.py
 - Modify historical.tables in R [REpipop]/share/platform/fr.r
 - Recreate views & functions ./sw_dashboard.sql

 - Empty invitations from past season
   ```bash
	run ./manage sw_invitation_cleanup
   ```

 - Empty badges data
    * Copy last year table dashboard_userbadge[season]
	* Create new empty one CREATE TABLE dashboard_userbadge (LIKE dashboard_userbadge[season] INCLUDING ALL)

 - Install new badges If same as previous year, just copy badges definitions
    ```sql
	 INSERT INTO dashboard_badge (name, label, description, datasource, attribute_to, season, compute_once, visible ) SELECT "name", "label", "description", "datasource", "attribute_to", [new season], "compute_once", "visible" from dashboard_badge where season=[previous season]
    ```

 - Prepare lastdata table
	 * Script [Repipop]/install/migrate[season].r
	 * copy previous year one, and adapt it if necesssary this will generate SQL to recreate view
	 * Recreate view pollster_results_intake_previousdata using the generated SQL

 - Update participation table
	```bash
	 Run ./manage grippenet_participation
	```

 - G-GrippeNet (Standby)
    * Backup previous season
    ```sql
	CREATE TABLE grippenet_pregnantcohort_2014 AS SELECT * FROM grippenet_pregnantcohort
	TRUNCATE TABLE grippenet_pregnantcohort
	#INSERT INTO grippenet_pregnantcohort (survey_user_id,date_created,active,change_channel,date_reminder,reminder_count) SELECT survey_user_id,date_created,active,change_channel,date_reminder,reminder_count FROM grippenet_pregnantcohort_2014 WHERE date_created >= '2015-09-01'
	# Ajout de celle dont l'inscription
	INSERT INTO grippenet_pregnantcohort (survey_user_id,date_created,active,change_channel,date_reminder,reminder_count) SELECT survey_user_id,date_created,active,change_channel,date_reminder,reminder_count FROM grippenet_pregnantcohort_2015 WHERE survey_user_id in(
		select survey_user_id from grippenet_pregnantcohort_2015 p left join survey_surveyuser s on s.id=p.survey_user_id left join (select global_id, min(timestamp) min_date, max(timestamp) max_date from pollster_results_intake_2015 where "Q12"=0 group by global_id) i on i.global_id=s.global_id
		where min_date >= '2016-06-01'
		)
	```
 - Anonymization of old (> 18 month participants)

 - Trunc data tables
	```sql
	TRUNCATE TABLE pollster_results_intake;
	TRUNCATE TABLE pollster_results_weekly;
	TRUNCATE TABLE dashboard_userbadge;
	TRUNCATE TABLE pollster_results_awareness;
	```

 - Deactivate Wait Launch message in [epipop]/local_settings.py
	```python
	 SURVEY_WAIT_LAUNCH = False
	```
  - Re grant for Statisitician
    ./pgperms

  - Run Start script
    ```bash
      ./manage grippenet_start
    ```

 - Run cron script to recreate data
 ```bash
   ./cron quotidien
   ./cron symptomes
 ```

 - Reactivate cron jobs if needed
   * counter
   * quotidien
   * symptomes
   