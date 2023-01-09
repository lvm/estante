# Estante

A toy DB for toying purposes


## How To

```
from estante import Estante

db = Estante("demo.db")

# to remove all Items
db.clear()

# this is the equivalent of an Items, a List of Item
items = [dict(id=1, title="hello"), dict(id=2, title="bye"), dict(id=3, title="mono")]

# that can be inserted as a batch, that will return a list of UUIDs as str
item_ids = db.batch_insert(items)

# or individually, which returns a single UUID as str
fourth_item = db.insert(dict(id=4, tilte="las oen"))

# it's possible to obtain just one
print(db.get(fourth_item))

# also update it
db.update(fourth_item, dict(id=4, title="last one"))
print(db.get(fourth_item))

# this way will show all four of them
print(db.all())

# also can be filtered using lookups
print(db.filter(title__endswith="e"))
print(db.filter(title__endswith="o"))

# or Item keys
print(db.filter(id=2))

# or exclude Items following the same logic
print(db.exclude(id=1))

# and finally, don't forget to sync or close
db.sync() # or db.close()

```

## Test

```
$ python3 -m unitest discover tests
```

## LICENSE

See [LICENSE](LICENSE)