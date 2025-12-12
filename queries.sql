SELECT 
    'Browns' as Team,
    CASE WHEN "12_Percent_Score" <= 12 THEN 'Met Rule' ELSE 'Failed Rule' END as Rule_Status,
    COUNT(*) as Games,
    ROUND(AVG(Win_Loss_Bool) * 100, 1) as Win_Percentage
FROM browns_opp_data
GROUP BY Rule_Status
UNION ALL
SELECT 
    'Opponents' as Team,
    CASE WHEN "Opp_12_Percent_Score" <= 12 THEN 'Met Rule' ELSE 'Failed Rule' END as Rule_Status,
    COUNT(*) as Games,
    ROUND(AVG(Opp_Is_Win) * 100, 1) as Win_Percentage
FROM browns_opp_data
GROUP BY Rule_Status;



SELECT 
    Result as Outcome,
    ROUND(AVG(Sacks), 1) as Avg_Sacks,
    ROUND(AVG(Turnovers), 1) as Avg_Turnovers,
    ROUND(AVG(Penalties), 1) as Avg_Penalties
FROM browns_opp_data
GROUP BY Result;



-- Randomize Browns Drops (Amari Cooper Era vs Post-Trade)
-- Week 1-6: Randomly 4 or 5 drops
-- Week 7+: Randomly 1 or 2 drops
UPDATE browns_opp_data
SET Est_Drops = CASE 
    WHEN Week <= 6 THEN (ABS(RANDOM()) % 2) + 4 
    ELSE (ABS(RANDOM()) % 2) + 1
END;

-- Randomize Opponent Drops
-- Randomly 2, 3, or 4 drops per game
UPDATE browns_opp_data
SET Opp_Est_Drops = (ABS(RANDOM()) % 3) + 2;

-- Recalculate 12% Scores for both teams
UPDATE browns_opp_data
SET 
    Total_Critical_Errors = Sacks + Turnovers + Penalties + Est_Drops,
    "12_Percent_Score" = ROUND((CAST((Sacks + Turnovers + Penalties + Est_Drops) AS FLOAT) / Total_Plays) * 100, 2),
    Opp_Total_Errors = Opp_Sacks + Opp_Turnovers + Opp_Penalties + Opp_Est_Drops,
    "Opp_12_Percent_Score" = ROUND((CAST((Opp_Sacks + Opp_Turnovers + Opp_Penalties + Opp_Est_Drops) AS FLOAT) / Opp_Total_Plays) * 100, 2);

-- Generate the "Rule Validity" Report
SELECT 
    Week,
    Opponent,
    Result,
    -- Browns Data
    Est_Drops AS "Browns Drops",
    "12_Percent_Score" AS "Browns Score",
    CASE 
        WHEN "12_Percent_Score" <= 12 THEN 'Met' 
        ELSE 'Failed' 
    END AS "Browns Status",
    CASE 
        WHEN ("12_Percent_Score" <= 12 AND Result = 'W') OR ("12_Percent_Score" > 12 AND Result = 'L') THEN 'Valid'
        ELSE 'Invalid'
    END AS "Browns Validity",
    -- Opponent Data
    Opp_Est_Drops AS "Opp Drops",
    "Opp_12_Percent_Score" AS "Opp Score",
    CASE 
        WHEN "Opp_12_Percent_Score" <= 12 THEN 'Met' 
        ELSE 'Failed' 
    END AS "Opp Status",
    -- Opponent Validity: Valid if they Met Rule & Won (Browns Lost) OR Failed Rule & Lost (Browns Won)
    CASE 
        WHEN ("Opp_12_Percent_Score" <= 12 AND Result = 'L') OR ("Opp_12_Percent_Score" > 12 AND Result = 'W') THEN 'Valid'
        ELSE 'Invalid'
    END AS "Opp Validity"
FROM browns_opp_data
ORDER BY Week;



SELECT 
    CASE 
        WHEN "12_Percent_Score" < "Opp_12_Percent_Score" THEN 'Cleaner Than Opponent' 
        ELSE 'Dirtier Than Opponent' 
    END AS Relative_Performance,
    COUNT(*) AS Games,
    SUM(CASE WHEN Result = 'W' THEN 1 ELSE 0 END) AS Wins,
    ROUND(AVG(CASE WHEN Result = 'W' THEN 1.0 ELSE 0.0 END) * 100, 1) AS Win_Percentage
FROM browns_opp_data
GROUP BY Relative_Performance;