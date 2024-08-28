import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
import io

# Datos CSV
csv_data = """Year;ENTIDAD;Cable modem (coaxial);DSL;Optic Fiber;Other Technologies
2015;Baja California;50%;44%;4%;2%
2015;Coahuila de Zaragoza;34%;55%;7%;4%
2015;Chihuahua;39%;52%;5%;3%
2015;Ciudad de México;36%;39%;23%;2%
2015;Guanajuato;38%;53%;6%;3%
2015;Jalisco;32%;53%;14%;1%
2015;Estado de México;25%;64%;10%;0.4%
2015;Nuevo León;45%;34%;19%;3%
2015;Sonora;55%;41%;3%;1%
2015;Veracruz de Ignacio de la Llave;37%;58%;2%;2%
2016;Baja California;50%;40%;9%;1%
2016;Coahuila de Zaragoza;49%;43%;7%;2%
2016;Chihuahua;24%;56%;17%;2%
2016;Ciudad de México;39%;31%;29%;1%
2016;Guanajuato;41%;47%;10%;2%
2016;Jalisco;32%;46%;22%;1%
2016;Estado de México;26%;58%;16%;0%
2016;Nuevo León;45%;30%;24%;1%
2016;Sonora;53%;40%;6%;0%
2016;Veracruz de Ignacio de la Llave;36%;56%;7%;1%
2017;Baja California;51%;37%;12%;1%
2017;Coahuila de Zaragoza;41%;49%;9%;1%
2017;Chihuahua;42%;39%;18%;1%
2017;Ciudad de México;39%;27%;34%;1%
2017;Guanajuato;45%;42%;12%;1%
2017;Jalisco;36%;40%;24%;0%
2017;Estado de México;30%;50%;20%;0%
2017;Nuevo León;46%;25%;28%;1%
2017;Sonora;62%;32%;6%;0%
2017;Veracruz de Ignacio de la Llave;41%;50%;9%;0%
2018;Baja California;51%;34%;15%;0.1%
2018;Coahuila de Zaragoza;29%;57%;14%;0.5%
2018;Chihuahua;43%;36%;21%;0.3%
2018;Ciudad de México;41%;24%;35%;0.2%
2018;Guanajuato;46%;39%;15%;0.3%
2018;Jalisco;37%;37%;26%;0.1%
2018;Estado de México;32%;46%;22%;0.0%
2018;Nuevo León;51%;23%;26%;0.3%
2018;Sonora;63%;30%;7%;0.1%
2018;Veracruz de Ignacio de la Llave;42%;46%;11%;0.1%
2019;Baja California;51%;28%;21%;0%
2019;Coahuila de Zaragoza;46%;40%;14%;0%
2019;Chihuahua;43%;29%;29%;0%
2019;Ciudad de México;40%;20%;40%;0%
2019;Guanajuato;48%;35%;17%;0%
2019;Jalisco;38%;33%;29%;0%
2019;Estado de México;35%;39%;27%;0%
2019;Nuevo León;49%;19%;32%;0%
2019;Sonora;66%;27%;7%;0%
2019;Veracruz de Ignacio de la Llave;43%;42%;14%;0%
2020;Baja California;46%;23%;31%;0.0%
2020;Coahuila de Zaragoza;43%;32%;25%;0.0%
2020;Chihuahua;40%;23%;37%;0.0%
2020;Ciudad de México;41%;15%;44%;0.0%
2020;Guanajuato;45%;30%;25%;0.0%
2020;Jalisco;38%;29%;33%;0.0%
2020;Estado de México;38%;28%;32%;0.0%
2020;Nuevo León;54%;15%;31%;0.0%
2020;Sonora;61%;25%;14%;0.0%
2020;Veracruz de Ignacio de la Llave;40%;37%;23%;0.0%"""

# Cargar datos en un DataFrame
df = pd.read_csv(io.StringIO(csv_data), sep=';')

# Convertir porcentajes a números flotantes
for col in df.columns[2:]:
    df[col] = df[col].str.rstrip('%').astype('float') / 100.0

# 1. Gráfico de tendencias
plt.figure(figsize=(12, 6))
for tech in df.columns[2:]:
    yearly_avg = df.groupby('Year')[tech].mean()
    plt.plot(yearly_avg.index, yearly_avg.values, marker='o', label=tech)

plt.title('Technology Adoption Trends (2015-2020)')
plt.xlabel('Year')
plt.ylabel('Average Percentage ')
plt.legend()
plt.grid(True)
plt.savefig('trends.png')
plt.close()

# 2. Análisis de correlación
correlation_matrix = df[df.columns[2:]].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
plt.title('Correlation Matrix between Technologies')
plt.savefig('correlation.png')
plt.close()

# 3. Análisis de la tasa de crecimiento
growth_rates = {}
for tech in df.columns[2:]:
    initial = df[df['Year'] == 2015][tech].mean()
    final = df[df['Year'] == 2020][tech].mean()
    growth_rate = (final - initial) / initial
    growth_rates[tech] = growth_rate

plt.figure(figsize=(10, 6))
plt.bar(growth_rates.keys(), growth_rates.values())
plt.title('Growth Rate by Technology (2015-2020)')
plt.ylabel('Growth Rate')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('Growth_Rate.png')
plt.close()

# 4. Análisis de varianza (ANOVA)
f_values = {}
p_values = {}
for tech in df.columns[2:]:
    groups = [group[tech].values for name, group in df.groupby('Year')]
    f_value, p_value = stats.f_oneway(*groups)
    f_values[tech] = f_value
    p_values[tech] = p_value

print("Resultados del Análisis de Varianza (ANOVA):")
for tech in df.columns[2:]:
    print(f"{tech}:")
    print(f"  F-value: {f_values[tech]:.4f}")
    print(f"  p-value: {p_values[tech]:.4f}")
    print()

# 5. Gráfico de cajas para visualizar la distribución por año
plt.figure(figsize=(12, 6))
sns.boxplot(x='Year', y='value', hue='variable', data=pd.melt(df, id_vars=['Year', 'ENTIDAD'], value_vars=df.columns[2:]))
plt.title('Distribution of Technologies by Year')
plt.ylabel('Percentaje')
plt.xticks(rotation=0)
plt.legend(title='Technology', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('distribution.png')
plt.close()

print("The following image files have been generated:")
print("1. trends_technology.png")
print("2. correlation_technologies.png")
print("3. growth_rate.png")
print("4. technology_distribution.png")