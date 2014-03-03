SELECT count(global_id)
FROM (
SELECT W.global_id, min(W.timestamp) AS first, max(W.timestamp) AS latest, count(*)::integer AS rate FROM epidb_results_weekly W WHERE date_trunc('day', W.timestamp) > '2012-11-01' AND W.country = 'ES'
GROUP BY W.global_id) AS data WHERE data.rate >=3 AND ( (data.latest::date - data.first::date) / data.rate::float) < 21;
