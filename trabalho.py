import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# 1. Carregar o CSV
df = pd.read_csv("IEA-EV-dataEV salesHistoricalCars.csv")

# 2. Mostrar as primeiras linhas
print("Visualização inicial:")
print(df.head())

# 3. Verificar colunas e valores nulos
print("\nColunas do dataset:", df.columns.tolist())
print("\nDados faltantes por coluna:\n", df.isnull().sum())

# 4. Filtrar apenas registros históricos de vendas na Austrália
df_aus = df[
    (df['region'] == 'Australia') &
    (df['category'] == 'Historical') &
    (df['parameter'] == 'EV sales') &
    (df['mode'] == 'Cars') &
    (df['unit'] == 'Vehicles')
]

# 5. Agrupar por ano e somar as vendas
df_grouped = df_aus.groupby('year')['value'].sum().reset_index()

# 6. Plotar gráfico de vendas ao longo dos anos
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_grouped, x='year', y='value', marker='o')
plt.title('Vendas de Carros Elétricos na Austrália (Histórico)')
plt.xlabel('Ano')
plt.ylabel('Unidades Vendidas')
plt.grid(True)
plt.tight_layout()
plt.savefig('grafico_vendas_australia.png')
plt.show()

# 7. Exemplo de modelo de regressão
df_model = df[
    (df['parameter'] == 'EV sales') &
    (df['unit'] == 'Vehicles')
].dropna()

# Preparar dados
df_model = pd.get_dummies(df_model, columns=['region', 'powertrain'])
X = df_model[['year'] + [col for col in df_model.columns if col.startswith('region_') or col.startswith('powertrain_')]]
y = df_model['value']

# Treinar modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Avaliação
mse = mean_squared_error(y_test, y_pred)
print(f"\nErro Quadrático Médio (MSE) do modelo preditivo: {mse:.2f}")
