import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import glob
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans

#from zipfile import ZipFile
# Create a ZipFile Object and load sample.zip in it
#with ZipFile('media/data/sensor.zip', 'r') as zipObj:
   # Extract all the contents of zip file in current directory
#   zipObj.extractall('media/data/')

list_of_files = glob.glob('media/data/*')
latest_file = max(list_of_files, key=os.path.getctime)


print("1250")
data = pd.DataFrame()
data = pd.read_csv(latest_file,
                        sep=',', encoding='UTF-8', low_memory=False)
#os.remove('media/data/sensor.csv')
print("1251")
def registros():
    # count number of rows
    registros = data.shape[0]
    #print("¿Cuántas columnas en el dataset hay? ", registros)
    return registros
print("1252")
def variables():
    # count number of rows
    variables = data.shape[1]
    #print("¿Cuántos variables en el dataset hay? ", variables)
    return variables
print("1253")
def sensores():
    # count number of columns that column names begin with 'sensor'
    sensores = data.filter(regex='sensor').shape[1]
    #print("¿Cuántos sensores de prueba hay? ", sensores)
    return sensores
print("1254")
# number of missing values in total
def missing_values():
    missing_values = data.isnull().sum().sum()
    #print("¿Cuántos valores faltantes hay en el dataset? ", missing_values)
    return missing_values
print("1255")
# we see that one column (sensor_15) has no values therefore we will delete that column 
data_clean = data.drop('sensor_15', axis = 1)
# Al sensor 50 también le falta el 34,95% de los datos, así que también eliminaremos esa columna. 
data_clean = data_clean.drop('sensor_50', axis =1) 
# Borraremos sensor_00 y sensor_51 a los que les faltan cerca del 6-7% de sus datos. 
# así como la columna Unnamed:0 que es esencialmente el duplicado de la columna índice.
data_clean = data_clean.drop('Unnamed: 0', axis =1)
data_clean = data_clean.drop('sensor_00', axis =1) 
data_clean = data_clean.drop('sensor_51', axis =1) 
print("1256")
def data_clean_df():
    return data_clean

print("1257")
def plot_missing_values():
    # plot a heatmap of the missing values
    plt.figure(figsize=(12,10))
    sns.heatmap(data.isna().transpose(),
                cmap='Greys',
                cbar_kws={'label': 'Faltan datos'})
    plt.title('Mapa de datos faltantes')
    plt.ylabel('Sensores')
    plt.xlabel('Registros')
    plt.savefig('static/graficas/missing.png')
    
def pie_plot_machine_status():
    # pie chart of machine status
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8,5))
    data_clean.groupby('machine_status').size().plot(kind='barh', ax=ax1, color=['black', 'grey', 'darkgrey'])
    data_clean.groupby('machine_status').size().plot(kind='pie', ax=ax2, autopct='%.4f%%', colors=['black', 'grey', 'darkgrey'])
    ax1.set_title('Gráfico de barras')
    # xlabel 90 degrees
    ax1.set_xlabel('', rotation=90)
    ax2.set_title('Gráfico circular')
    ax2.set_ylabel('')
    plt.savefig('static/graficas/pie_machine_status.png')
    
def html_table_descripcion():
    data_descrp = data_clean.describe().T.reset_index()
    return data_descrp


# - mapping normal, recovering and broken to 1,0.5,0
m = {'NORMAL': 1, 'RECOVERING': 0.5, 'BROKEN': 0}  # mapping
data_clean['stat'] = data_clean['machine_status'].map(m)  # mapping
data_clean['rol'] = data_clean['stat'].rolling(2).mean()  # rolling mean

# Seleccionamos las columnas de los sensores
sensor_cols = data_clean.iloc[:,1:52]
# drop machine_status column in sensor_cols
sensor_cols = sensor_cols.drop('machine_status', axis=1)

# clasificamos los sensores en 3 grupos:
broken_rows = data_clean[data_clean['machine_status']=='BROKEN']
recovery_rows = data_clean[data_clean['machine_status']=='RECOVERING']
normal_rows = data_clean[data_clean['machine_status']=='NORMAL']
machine_status_col = data_clean['machine_status']


# This visualization loop was inspired from JANANI KARIYAWASAM found at 
# https://www.kaggle.com/code/jananikariyawasam/data-cleaning-and-feature-engineering

def plot_sensors():
    for sensor in sensor_cols:
        plot = plt.figure(figsize=(15,3))
        plot = plt.plot(recovery_rows[sensor], linestyle='none', marker='o', color='yellow', markersize=5)
        plot = plt.plot(data_clean[sensor], color='grey')
        plot = plt.plot(broken_rows[sensor], linestyle='none', marker='X', color='red', markersize=14)
        plot = plt.title(sensor)
        plt.xlim((-1000,177000))
        plt.savefig('static/graficas/'+sensor+'.png')
        plt.close()
        

        
data_clean_corr = data_clean.corr(numeric_only=True)
def corr_heat_map():
    # Heatmap for the entire data

    fig, ax = plt.subplots(1, 1, figsize=(15, 12))
    

    mask = np.zeros_like(data_clean_corr, dtype=np.bool_)
    mask[np.triu_indices_from(mask)] = True

    sns.heatmap(data_clean_corr, ax=ax,
            square=True, center=0, linewidth=1,
            cmap='Greys',
            cbar_kws={'shrink': .82},
            mask=mask,
            annot=True,
            annot_kws={'size':7}
            )
    ax.set_title(f'Correlation', loc='left', fontweight='bold')
    plt.savefig('static/graficas/corr_heatmap.png')
    plt.close()        

# Correlation between the sensors and the machine status
l = [] # empty list to store the columns with correlation > 0.75
for i in data_clean_corr['stat'].index:
    if data_clean_corr['stat'][i] > 0.75:
        print(i)
        l.append(i)
        
# drop last 2 columns
l.pop()
#l.pop()
    
print(l)
# add 'timestamp', 'machine_status' to the list
l = ['timestamp', 'machine_status'] + l

#print(data_clean.info())
#print(data_clean.head())
# convert wide to long format
def melt_data():
    # select only the sensor columns with major correlation
    corr_data_clean = data_clean[l]
    
    corr_data_clean['timestamp'] = pd.to_datetime(corr_data_clean['timestamp'])
    return corr_data_clean



# Split into training data and test data
X = data_clean[['sensor_02', 'sensor_04', 'sensor_06', 'sensor_10', 'sensor_11', 'sensor_12']]
y = data_clean['machine_status']

# train test split with 60% training data and 40% test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

X_train_y_train = pd.concat([X_train, y_train], axis=0)

def melt_data_1():
    # select only the sensor columns with major correlation
    corr_data_clean = X_train_y_train
    return corr_data_clean


#fill NA's with forward fill propogation
X_train = X_train.fillna(method='ffill')
X_test = X_test.fillna(method='ffill')

# normalize data 
normalize = Normalizer()
X_train = normalize.fit_transform(X_train)
X_train = pd.DataFrame(X_train)
X_train.columns = X.columns

# Kmeans clustering
# visualize errors based on number of clusters
model = KMeans(n_init=10, max_iter=300)
model.fit(X_train, y_train)

# make predictions on validation dataset
predictions = model.predict(X_test)

# pickle the model
pd.to_pickle(model, 'media/model.pickle')

# unpickle the model
model = pd.read_pickle('media/model.pickle')

# take input from user
#sensor_02 = float(input('Ingrese el valor del sensor 02: '))
#sensor_04 = float(input('Ingrese el valor del sensor 04: '))
#sensor_06 = float(input('Ingrese el valor del sensor 06: '))
#sensor_10 = float(input('Ingrese el valor del sensor 10: '))
#sensor_11 = float(input('Ingrese el valor del sensor 11: '))
#sensor_12 = float(input('Ingrese el valor del sensor 12: '))

#result = model.predict([[sensor_02, sensor_04, sensor_06, sensor_10, sensor_11, sensor_12]]) # make prediction
#print(result)
