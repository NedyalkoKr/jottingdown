from django.contrib.postgres.search import SearchVector
from django.db import migrations


def compute_search_vector(apps, schema_editor):
  Topic = apps.get_model("topics", "Topic")
  Topic.objects.update(search_vector=SearchVector("content", "title",))


class Migration(migrations.Migration):

  dependencies = [
    ("topics", "0003_topic_content"),
  ]

  operations = [
    migrations.RunSQL(
      sql="""
      CREATE TRIGGER search_vector_trigger
      BEFORE INSERT OR UPDATE OF "content", "title", search_vector
      ON topics
      FOR EACH ROW EXECUTE PROCEDURE
      tsvector_update_trigger(
        search_vector, 'pg_catalog.english', content, title
      );
      UPDATE topics SET search_vector = NULL;
      """,
      reverse_sql="""
      DROP TRIGGER IF EXISTS search_vector_trigger
      ON topics;
      """,
    ),
    migrations.RunPython(
      compute_search_vector, reverse_code=migrations.RunPython.noop
    ),
  ]