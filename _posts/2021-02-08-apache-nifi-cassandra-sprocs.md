---
layout: post
tags: [cassandra, nifi]
---
<h1>Apache NiFi and Cassandra</h1>

Looked at Apache NiFi for the first time in a long time as someone didn't know if it had support for stored procedures or not. I looked up the latest source
and sure enough I see no stored procedures used for any of the statements. Looking at the [PutCassandraRecord.java](https://github.com/apache/nifi/blob/953327cdf587c6b68765c0d32508873d8a0031e7/nifi-nar-bundles/nifi-cassandra-bundle/nifi-cassandra-processors/src/main/java/org/apache/nifi/processors/cassandra/PutCassandraRecord.java) I see inserts and updates are just statements that are never prepared:

                    query = generateInsert(cassandraTable, schema, recordContentMap);
and 

                    query = generateUpdate(cassandraTable, schema, updateKeys, updateMethod, recordContentMap);

digging into the method calls we also find no reference

```java

 protected Statement generateUpdate(String cassandraTable, RecordSchema schema, String updateKeys, String updateMethod, Map<String, Object> recordContentMap) {
        Update updateQuery;

        // Split up the update key names separated by a comma, should not be empty
        final Set<String> updateKeyNames;
        updateKeyNames = Arrays.stream(updateKeys.split(","))
                .map(String::trim)
                .filter(StringUtils::isNotEmpty)
                .collect(Collectors.toSet());
        if (updateKeyNames.isEmpty()) {
            throw new IllegalArgumentException("No Update Keys were specified");
        }

        // Verify if all update keys are present in the record
        for (String updateKey : updateKeyNames) {
            if (!schema.getFieldNames().contains(updateKey)) {
                throw new IllegalArgumentException("Update key '" + updateKey + "' is not present in the record schema");
            }
        }

        // Prepare keyspace/table names
        if (cassandraTable.contains(".")) {
            String[] keyspaceAndTable = cassandraTable.split("\\.");
            updateQuery = QueryBuilder.update(keyspaceAndTable[0], keyspaceAndTable[1]);
        } else {
            updateQuery = QueryBuilder.update(cassandraTable);
        }

        // Loop through the field names, setting those that are not in the update key set, and using those
        // in the update key set as conditions.
        for (String fieldName : schema.getFieldNames()) {
            Object fieldValue = recordContentMap.get(fieldName);

            if (updateKeyNames.contains(fieldName)) {
                updateQuery.where(QueryBuilder.eq(fieldName, fieldValue));
            } else {
                Assignment assignment;
                if (SET_TYPE.getValue().equalsIgnoreCase(updateMethod)) {
                    assignment = QueryBuilder.set(fieldName, fieldValue);
                } else if (INCR_TYPE.getValue().equalsIgnoreCase(updateMethod)) {
                    assignment = QueryBuilder.incr(fieldName, convertFieldObjectToLong(fieldName, fieldValue));
                } else if (DECR_TYPE.getValue().equalsIgnoreCase(updateMethod)) {
                    assignment = QueryBuilder.decr(fieldName, convertFieldObjectToLong(fieldName, fieldValue));
                } else {
                    throw new IllegalArgumentException("Update Method '" + updateMethod + "' is not valid.");
                }
                updateQuery.with(assignment);
            }
        }
        return updateQuery;
    }
```

insertQuery

```java
    private Statement generateInsert(String cassandraTable, RecordSchema schema, Map<String, Object> recordContentMap) {
        Insert insertQuery;
        if (cassandraTable.contains(".")) {
            String[] keyspaceAndTable = cassandraTable.split("\\.");
            insertQuery = QueryBuilder.insertInto(keyspaceAndTable[0], keyspaceAndTable[1]);
        } else {
            insertQuery = QueryBuilder.insertInto(cassandraTable);
        }
        for (String fieldName : schema.getFieldNames()) {
            Object value = recordContentMap.get(fieldName);

            if (value != null && value.getClass().isArray()) {
                Object[] array = (Object[])value;

                if (array.length > 0 && array[0] instanceof Byte) {
                    Object[] temp = (Object[]) value;
                    byte[] newArray = new byte[temp.length];
                    for (int x = 0; x < temp.length; x++) {
                        newArray[x] = (Byte) temp[x];
                    }
                    value = ByteBuffer.wrap(newArray);
                }
            }
            insertQuery.value(fieldName, value);
        }
        return insertQuery;
    }
```

So we can see with those two methods there is no way for ingest to be using prepared statements with some code restructuring and retaining a prepared statement cache. Looking at the [QueryCassandra.java](https://github.com/apache/nifi/blob/953327cdf587c6b68765c0d32508873d8a0031e7/nifi-nar-bundles/nifi-cassandra-bundle/nifi-cassandra-processors/src/main/java/org/apache/nifi/processors/cassandra/QueryCassandra.java) we can see just a simple string is used, and passed to the query, so not prepared again.

        final String selectQuery = context.getProperty(CQL_SELECT_QUERY).evaluateAttributeExpressions(fileToProcess).getValue();

        final ResultSetFuture queryFuture = connectionSession.executeAsync(selectQuery);


