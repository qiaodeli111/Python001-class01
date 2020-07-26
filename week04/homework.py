import pandas as pd
import numpy as np

group = ['x','y','z']
df = pd.DataFrame({
    "id":[group[x] for x in np.random.randint(0,len(group),10)] ,
    "age":np.random.randint(15,50,10)
    })

# 1. SELECT * FROM data;
# 
df
# 2. SELECT * FROM data LIMIT 10;
df.head(10)
# 
# 3. SELECT id FROM data;  //id 是 data 表的特定一列
df['id']
# 
# 4. SELECT COUNT(id) FROM data;
df['CRIM'].count()
# 
# 5. SELECT * FROM data WHERE id<1000 AND age>30;
df[(df['id']<1000) & (df['age']>30)]
# 
# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
df.groupby('id').count()
# 
# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
pd.merge(t1, t2, on='id', how='inner')
# 
# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
pd.concat([table1, table2])
# 
# 9. DELETE FROM table1 WHERE id=10;
df[ df['id'] != 10]
# 
# 10. ALTER TABLE table1 DROP COLUMN column_name;
df.drop('column_name', axis=1)
# 