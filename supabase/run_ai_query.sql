-- OvenOS AI Insights: safe RPC for GPT-4o-generated SELECT queries
-- Deploy: paste into Supabase SQL Editor and run
CREATE OR REPLACE FUNCTION run_ai_query(query_text TEXT)
RETURNS JSON LANGUAGE plpgsql SECURITY DEFINER SET search_path=public
AS $$
DECLARE result JSON; safe_query TEXT;
BEGIN
  IF NOT (upper(trim(query_text)) LIKE 'SELECT%') THEN
    RAISE EXCEPTION 'Only SELECT statements are permitted.';
  END IF;
  IF upper(query_text) LIKE '%DROP%' OR upper(query_text) LIKE '%DELETE%'
     OR upper(query_text) LIKE '%INSERT%' OR upper(query_text) LIKE '%UPDATE%'
     OR upper(query_text) LIKE '%TRUNCATE%' OR upper(query_text) LIKE '%EXECUTE%' THEN
    RAISE EXCEPTION 'Blocked keyword detected in query.';
  END IF;
  safe_query := format(
    'SELECT json_agg(t) FROM (SELECT * FROM (%s) sub LIMIT 100) t',
    query_text
  );
  EXECUTE safe_query INTO result;
  RETURN COALESCE(result, '[]'::json);
EXCEPTION WHEN OTHERS THEN
  RETURN json_build_object('error', SQLERRM, 'detail', SQLSTATE);
END;
$$;
REVOKE ALL ON FUNCTION run_ai_query(TEXT) FROM PUBLIC;
REVOKE ALL ON FUNCTION run_ai_query(TEXT) FROM anon;
REVOKE ALL ON FUNCTION run_ai_query(TEXT) FROM authenticated;
GRANT EXECUTE ON FUNCTION run_ai_query(TEXT) TO service_role;
