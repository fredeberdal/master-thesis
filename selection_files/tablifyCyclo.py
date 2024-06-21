from tabulate import tabulate

data = [
  {
    "file_name": "src\\Apollo-Server\\index.js",
    "cyclo": 59
  },
  {
    "file_name": "src\\Components\\AboutWineComponent.tsx",
    "cyclo": 39
  },
  {
    "file_name": "src\\Apollo-Server\\index.tsx",
    "cyclo": 11
  },
  {
    "file_name": "src\\pages\\Homepage.tsx",
    "cyclo": 9
  },
  {
    "file_name": "src\\Components\\FilterComponent.tsx",
    "cyclo": 8
  },
  {
    "file_name": "src\\Components\\WineComponent.tsx",
    "cyclo": 6
  },
  {
    "file_name": "src\\Components\\HeaderComponent.tsx",
    "cyclo": 3
  },
  {
    "file_name": "src\\contexts\\FavoriteContext.tsx",
    "cyclo": 3
  }
]

# Prep the data
table_data = [[entry["file_name"], entry["cyclo"]] for entry in data]

# Print data in table format
print(tabulate(table_data, headers=['File', 'Cyclomatic'], tablefmt='grid'))