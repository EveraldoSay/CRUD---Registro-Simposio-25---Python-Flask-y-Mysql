from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import re
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'mysecretkey'

# CONFIGURACION, CONEXION BD MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ingenieria'
mysql = MySQL(app)


#RUTA INDEX

@app.route('/')
def index():
    try:
        cur = mysql.cursor()
        # Obtenenemos las estadísticas de registros por rango de edad
        cur.execute(''' 
            SELECT 
                CASE
                    WHEN TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) BETWEEN 0 AND 20 THEN '0-20'
                    WHEN TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) BETWEEN 21 AND 40 THEN '21-40'
                    WHEN TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) BETWEEN 41 AND 60 THEN '41-60'
                    WHEN TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) > 60 THEN 'Mayores de 60'
                END AS rango_edad,
                COUNT(*) AS cantidad
            FROM registros
            GROUP BY rango_edad
            ORDER BY FIELD(rango_edad, '0-20', '21-40', '41-60', 'Mayores de 60');
        ''')
        estadisticas = cur.fetchall()
        cur.close()
        # Verificamos si los datos se recuperan correctamente
        print(estadisticas)  # Deberiamos ver algo como [('0-20', 150), ('21-40', 300), ...]
        # Mandemos datos a la plantilla/vista
        return render_template('index.html', estadisticas=estadisticas)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', estadisticas=[])


#RUTA VISTA REGISTROS - SELECT - VER

@app.route('/verRegistros')
def verRegistros():
    # Buscamos si existe
    search_query = request.args.get('q', '').strip()
    # Conectar a la base de datos
    cur = mysql.connection.cursor()
    # Contruyendo query SQL
    if search_query:
        # Buscar en entidades nombres y apellidos
        query = '''
            SELECT * FROM registros 
            WHERE CONCAT(primer_nombre, ' ', segundo_nombre, ' ', primer_apellido, ' ', segundo_apellido) LIKE %s
        '''
        cur.execute(query, (f"%{search_query}%",))
    else:
        # Si no hay búsqueda, cachamos todos lo registros
        cur.execute('SELECT * FROM registros')

    # Obtenemos los resultados
    registros = cur.fetchall()
    cur.close()

    # Redirigimos a vista SELECT - VER
    return render_template('verRegistros.html', registros=registros)



# RUTA CREATE

@app.route('/createRegistro', methods=['GET', 'POST'])
def create_registro():
    if request.method == 'POST':
        try:
            # Cachamos datos del formulario
            carnet_carrera = request.form.get('carnet_carrera', '')
            carnet_anio = request.form.get('carnet_anio', '')
            carnet_correlativo = request.form.get('carnet_correlativo', '')
            primer_nombre = request.form.get('primer_nombre', '')
            segundo_nombre = request.form.get('segundo_nombre', '')
            primer_apellido = request.form.get('primer_apellido', '')
            segundo_apellido = request.form.get('segundo_apellido', '')
            phone = request.form.get('phone', '')
            email = request.form.get('email', '').strip().lower()
            pagado = 1 if request.form.get('pagado') == 'Si' else 0
            fecha_nacimiento = request.form.get('fecha_nacimiento', '')

            # Validar que el año no sea mayor a 25, porque nadie tiene carnet del otro año
            try:
                carnet_anio = int(carnet_anio)
                if carnet_anio > 25:
                    flash('❌ El año no puede ser mayor a 25.', 'danger')
                    return render_template('createRegistro.html', 
                                           carnet_carrera=carnet_carrera, 
                                           carnet_anio=carnet_anio, 
                                           carnet_correlativo=carnet_correlativo, 
                                           primer_nombre=primer_nombre, 
                                           segundo_nombre=segundo_nombre, 
                                           primer_apellido=primer_apellido, 
                                           segundo_apellido=segundo_apellido,
                                           phone=phone, 
                                           email=email, 
                                           pagado=request.form.get('pagado', ''),
                                           fecha_nacimiento=fecha_nacimiento)
            except ValueError:
                flash('❌ El año del carnet debe ser un número válido.', 'danger')
                return render_template('createRegistro.html', 
                                       carnet_carrera=carnet_carrera, 
                                       carnet_anio=carnet_anio, 
                                       carnet_correlativo=carnet_correlativo, 
                                       primer_nombre=primer_nombre, 
                                       segundo_nombre=segundo_nombre, 
                                       primer_apellido=primer_apellido, 
                                       segundo_apellido=segundo_apellido,
                                       phone=phone, 
                                       email=email, 
                                       pagado=request.form.get('pagado', ''),
                                       fecha_nacimiento=fecha_nacimiento)

            # Validamos la fecha de nacimiento
            try:
                datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
            except ValueError:
                flash('❌ La fecha de nacimiento no es válida. Use el formato YYYY-MM-DD.', 'danger')
                return render_template('createRegistro.html', 
                                       carnet_carrera=carnet_carrera, 
                                       carnet_anio=carnet_anio, 
                                       carnet_correlativo=carnet_correlativo, 
                                       primer_nombre=primer_nombre, 
                                       segundo_nombre=segundo_nombre, 
                                       primer_apellido=primer_apellido, 
                                       segundo_apellido=segundo_apellido,
                                       phone=phone, 
                                       email=email, 
                                       pagado=request.form.get('pagado', ''),
                                       fecha_nacimiento=fecha_nacimiento)

            # Verificar si el carnet ya está registrado, notificamos
            cur = mysql.connection.cursor()
            cur.execute('SELECT COUNT(*) FROM registros WHERE Carnet_Carrera = %s AND Carnet_Anio = %s AND Carnet_Correlativo = %s', 
                         (carnet_carrera, carnet_anio, carnet_correlativo))
            carnet_count = cur.fetchone()[0]

            if carnet_count > 0:
                flash('❌ Este carnet ya está registrado. Intente con otro.', 'danger')
                cur.close()
                return render_template('createRegistro.html', 
                                       carnet_carrera=carnet_carrera, 
                                       carnet_anio=carnet_anio, 
                                       carnet_correlativo=carnet_correlativo, 
                                       primer_nombre=primer_nombre, 
                                       segundo_nombre=segundo_nombre, 
                                       primer_apellido=primer_apellido, 
                                       segundo_apellido=segundo_apellido,
                                       phone=phone, 
                                       email=email, 
                                       pagado=request.form.get('pagado', ''),
                                       fecha_nacimiento=fecha_nacimiento)

            # Insert correctamente entonces
            cur.execute('''
                INSERT INTO registros (Carnet_Carrera, Carnet_Anio, Carnet_Correlativo, Primer_Nombre, Segundo_Nombre, Primer_Apellido, Segundo_Apellido, Telefono, Correo, Pagado, Fecha_Nacimiento) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (carnet_carrera, carnet_anio, carnet_correlativo, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, phone, email, pagado, fecha_nacimiento))
            
            mysql.connection.commit()
            cur.close()

            flash('✅ Registro creado con éxito.', 'success')
            return redirect(url_for('verRegistros'))

        except Exception as e:
            flash(f'❌ Ocurrió un error: {str(e)}', 'danger')
            return render_template('createRegistro.html')

    return render_template('createRegistro.html')



# RUTA - EDIT - UPDATE

@app.route('/editRegistro/<string:carnet_carrera>/<int:carnet_anio>/<string:carnet_correlativo>', methods=['GET', 'POST'])
def edit_registro(carnet_carrera, carnet_anio, carnet_correlativo):
    try:
        with mysql.connection.cursor() as cur:
            # Buscar el registro actual
            cur.execute('''SELECT * FROM registros 
                           WHERE Carnet_Carrera = %s AND Carnet_Anio = %s AND Carnet_Correlativo = %s''', 
                           (carnet_carrera, carnet_anio, carnet_correlativo))
            registro = cur.fetchone()

            if registro is None:
                flash('❌ El registro no existe.', 'danger')
                return redirect(url_for('verRegistros'))

            if request.method == 'POST':
                # Obtenemos datos del formulario
                nuevo_carnet_carrera = request.form.get('carnet_carrera', '')
                nuevo_carnet_anio = request.form.get('carnet_anio', '')
                nuevo_carnet_correlativo = request.form.get('carnet_correlativo', '')
                primer_nombre = request.form.get('primer_nombre', '')
                segundo_nombre = request.form.get('segundo_nombre', '')
                primer_apellido = request.form.get('primer_apellido', '')
                segundo_apellido = request.form.get('segundo_apellido', '')
                telefono = request.form.get('telefono', '')
                correo = request.form.get('correo', '')
                pagado = 1 if request.form.get('pagado') == 'Si' else 0
                fecha_nacimiento = request.form.get('fecha_nacimiento', '')

                # Validar el año del carnet, tambien validando no mayor a año 25
                try:
                    nuevo_carnet_anio = int(nuevo_carnet_anio)
                    if nuevo_carnet_anio > 25:
                        flash('❌ El año del carnet no puede ser mayor a 25.', 'danger')
                        return render_template('editRegistro.html', registro=request.form)
                except ValueError:
                    flash('❌ El año del carnet debe ser un número válido.', 'danger')
                    return render_template('editRegistro.html', registro=request.form)

                # Validar la fecha de nacimiento
                try:
                    datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
                except ValueError:
                    flash('❌ La fecha de nacimiento no es válida. Use el formato YYYY-MM-DD.', 'danger')
                    return render_template('editRegistro.html', registro=request.form)

                # Verificar si el nuevo carnet si lo llegara a modificar para avisarle
                if (nuevo_carnet_carrera != carnet_carrera or 
                    nuevo_carnet_anio != carnet_anio or 
                    nuevo_carnet_correlativo != carnet_correlativo):
                    
                    cur.execute('''SELECT COUNT(*) FROM registros 
                                   WHERE Carnet_Carrera = %s AND Carnet_Anio = %s AND Carnet_Correlativo = %s''', 
                                   (nuevo_carnet_carrera, nuevo_carnet_anio, nuevo_carnet_correlativo))
                    carnet_existente = cur.fetchone()[0]

                    if carnet_existente > 0:
                        flash('❌ Este carnet ya está registrado. Intente con otro.', 'danger')
                        return render_template('editRegistro.html', registro=request.form)

                # Update Satisfactorio
                cur.execute('''UPDATE registros 
                               SET Carnet_Carrera = %s, Carnet_Anio = %s, Carnet_Correlativo = %s, 
                                   Primer_Nombre = %s, Segundo_Nombre = %s, Primer_Apellido = %s, Segundo_Apellido = %s, 
                                   Telefono = %s, Correo = %s, Fecha_Nacimiento = %s, Pagado = %s
                               WHERE Carnet_Carrera = %s AND Carnet_Anio = %s AND Carnet_Correlativo = %s''',
                            (nuevo_carnet_carrera, nuevo_carnet_anio, nuevo_carnet_correlativo, 
                             primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, telefono, correo, fecha_nacimiento, pagado, 
                             carnet_carrera, carnet_anio, carnet_correlativo))
                mysql.connection.commit()

                flash('✅ Registro actualizado con éxito.', 'success')
                return redirect(url_for('verRegistros'))

            # Convertir el registro a un diccionario para la plantilla
            registro_dict = {
                'carnet_carrera': registro[1],
                'carnet_anio': registro[2],
                'carnet_correlativo': registro[3],
                'primer_nombre': registro[4],
                'segundo_nombre': registro[5],
                'primer_apellido': registro[6],
                'segundo_apellido': registro[7],
                'telefono': registro[8],
                'correo': registro[9],
                'pagado': 'Si' if registro[10] == 1 else 'No',
                'fecha_nacimiento': registro[11]
            }

            return render_template('editRegistro.html', registro=registro_dict)

    except Exception as e:
        flash(f'❌ Ocurrió un error: {str(e)}', 'danger')
        return redirect(url_for('verRegistros'))


# RUTA - DELETE

@app.route('/deleteRegistro/<int:id_registro>', methods=['POST'])
def delete_registro(id_registro):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM registros WHERE Id_Registro = %s', (id_registro,))
    mysql.connection.commit()
    cur.close()
    flash('✅ Registro eliminado con éxito.', 'success')
    return redirect(url_for('verRegistros'))


#iniciar aplicación Flask
# Sin esto, la aplicación Flask no ejecutará automáticamente, y no se podra acceder al sitio web localmente.

if __name__ == '__main__':
    app.run(debug=True)
