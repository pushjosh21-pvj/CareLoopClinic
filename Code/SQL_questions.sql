-- SQL questions
-- Exported from Datapad on 2026-11-08. Open in MySQL Workbench and run with Ctrl+Shift+Enter.

-- Block 1
USE careloopclinic;

-- Block 2
SELECT * FROM appointments LIMIT 5;

-- Block 3
SELECT c.clinic_name, c.city, COUNT(a.appointment_id) as Total_Appointments, 
ROUND(SUM(a.no_show)/ COUNT(a.appointment_id)*100,1) as No_Show_Pct
FROM appointments as a
LEFT JOIN clinics as c
ON a.clinic_id = c.clinic_id
GROUP BY c.clinic_name, c.city
-- HAVING COUNT(a.appointment_id) > 95
ORDER BY No_Show_Pct DESC;

-- Block 4
WITH app_pvt AS (SELECT a.no_show, a.lead_days,
CASE 
WHEN a.lead_days <= 7 THEN '1-7 days'
WHEN a.lead_days <= 14 THEN '8-14 days'
WHEN a.lead_days <= 30 THEN '15-30 days'
ELSE '31+ days'
END as lead_day_buckets
FROM appointments as a
ORDER BY lead_days)

SELECT lead_day_buckets, 
COUNT(no_show) as Total_Appointments,
SUM(no_show) as Show_Appointments,
(100 - SUM(no_show) / COUNT(no_show) * 100) as No_Show_Pct
FROM app_pvt
GROUP BY lead_day_buckets
ORDER BY MIN(lead_days);

-- Block 5
SELECT COUNT(a.no_show) as Total_Appointments, 
SUM(a.no_show) as Show_Appointments, 
(100 - SUM(a.no_show)/ COUNT(a.no_show) * 100) as No_Show_Pct,
CASE 
WHEN a.lead_days <= 7 THEN '1-7 days'
WHEN a.lead_days <= 14 THEN '8-14 days'
WHEN a.lead_days <= 30 THEN '15-30 days'
ELSE '31+ days'
END as lead_day_buckets
FROM appointments as a
GROUP BY lead_day_buckets 
ORDER BY MIN(a.lead_days);

-- Block 6
WITH monthly as 
(
    SELECT SUBSTR(appt_date,1,7) as month, 
    COUNT(no_show) as Total_Appointments, 
    (100 - SUM(no_show)/ COUNT(no_show) * 100) as No_Show_Pct
    FROM appointments
    GROUP BY month
) 

SELECT *, 
    LAG(No_Show_Pct, 1, "-") OVER (ORDER BY month) as Pre_No_Show_Pct,
    (No_Show_Pct - LAG(No_Show_Pct, 1, "-") OVER (ORDER BY month)) as Pct_Change 
FROM monthly
ORDER BY month;

-- Block 7
SELECT 
c.city, 
c.clinic_name,
ROUND(SUM(a.no_show)/ COUNT(a.appointment_id)*100.0,1) as No_Show_Pct,
RANK() OVER (
    PARTITION BY c.city 
    ORDER BY ROUND(SUM(a.no_show) * 100.0 / COUNT(a.appointment_id),1) DESC
) as City_Rank
FROM appointments as a
LEFT JOIN clinics as c
ON a.clinic_id = c.clinic_id
GROUP BY c.clinic_name, c.city
ORDER BY c.city, City_Rank ASC;
