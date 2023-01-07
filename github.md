## Github

GitHub es una plataforma en línea que ofrece almacenamiento y control de versiones para proyectos de software. El control de versiones es un sistema que registra los cambios realizados en un archivo o conjunto de archivos a lo largo del tiempo, de modo que puedas recuperar versiones específicas más adelante.

Para utilizar GitHub, necesitarás instalar Git en tu ordenador. Git es una herramienta de línea de comandos que te permite trabajar con repositorios de código (es decir, colecciones de archivos). Un repositorio de código es un lugar donde se almacena y mantiene el código fuente de un proyecto, junto con todas las versiones del código y los registros de cambios.

Para empezar a utilizar GitHub, primero debes crear una cuenta en la plataforma y luego crear un nuevo repositorio. Una vez creado el repositorio, puedes subir tus archivos al repositorio utilizando Git. Cada vez que realices cambios en tus archivos y quieras guardar una nueva versión, debes "commit" (realizar un compromiso) los cambios y "push" (enviar) los cambios al repositorio de GitHub.

GitHub te permite trabajar de forma colaborativa con otros desarrolladores, ya que permite compartir repositorios y realizar "pull requests" (solicitudes de envío) para fusionar cambios realizados por otros en tu repositorio. También puedes utilizar GitHub para gestionar problemas y discutir cambios con otros desarrolladores.

En resumen, GitHub es una plataforma que te permite almacenar y controlar las versiones de tus proyectos de software de forma colaborativa y eficiente.


## AWS - Django

Para implementar un proyecto de Django en AWS a través de una instancia de EC2, puedes seguir los siguientes pasos:

    Crea una instancia de EC2 en la consola de AWS siguiendo las instrucciones de la plataforma. Asegúrate de elegir una imagen de AMI (Amazon Machine Image) que incluya Python y Django.

    Conecta a la instancia de EC2 utilizando SSH. Puedes hacerlo desde la consola de AWS o utilizando un cliente de SSH como PuTTY.

    Una vez conectado a la instancia de EC2, asegúrate de tener los paquetes necesarios para ejecutar tu proyecto de Django. Esto incluye Python, Django y cualquier otra dependencia que tu proyecto requiera. Puedes instalar estos paquetes utilizando pip.

    Descarga o sube tu proyecto de Django a la instancia de EC2. Puedes hacerlo utilizando un cliente SFTP como FileZilla o utilizando Git para clonar el repositorio del proyecto.

    Una vez que tengas tu proyecto en la instancia de EC2, debes configurar la base de datos. Si estás utilizando una base de datos SQLite, simplemente debes asegurarte de que la base de datos existe y está en el lugar correcto. Si estás utilizando una base de datos PostgreSQL o MySQL, debes crear una base de datos y un usuario en el servidor de base de datos y luego configurar tu proyecto de Django para conectarse a la base de datos utilizando las credenciales del usuario.

    Finalmente, debes configurar el servidor web para servir tu proyecto de Django. Puedes utilizar un servidor web como Apache o Nginx para hacerlo. Debes configurar el servidor web para que sirva los archivos estáticos del proyecto y redirija las solicitudes de URL a Django. Una vez que hayas configurado el servidor web, deberías poder acceder a tu proyecto de Django a través de un navegador web.

Es posible que debas realizar algunos pasos adicionales dependiendo de la configuración específica de tu proyecto y de la instancia de EC2 que hayas creado. Si tienes dificultades para implementar tu proyecto de Django en AWS, puedes consultar la documentación de Django y AWS o buscar ayuda en foros y comunidades en línea.


## Screen RC

Screen es una herramienta de terminal que permite ejecutar varias sesiones de terminal en una sola ventana y controlarlas de forma independiente. Para configurar screen, puedes utilizar un archivo de configuración llamado screenrc. Los comandos más comunes que puedes incluir en un archivo screenrc son:

    bind: permite asignar una secuencia de teclas a una acción o comando de screen. Por ejemplo, bind c screen -t nueva 0 asigna la secuencia de teclas C-a c a la creación de una nueva ventana.

    hardstatus: permite personalizar la línea de estado de screen, que se muestra en la parte inferior de la ventana. Por ejemplo, hardstatus alwayslastline "%{= wb} %H %{= wk} %?%-Lw%?%{+b}[%n*%f %t]%?(%u)%?%{-b}%+Lw %= %c %D %M %d %Y" muestra el hostname, el número de la ventana actual, el título de la ventana y la fecha y hora actual.

    startup_message off: desactiva el mensaje de bienvenida de screen al iniciar la aplicación.

    vbell off: desactiva el timbre visual de screen cuando se recibe una señal de terminal.

    escape ^Xb: establece la secuencia de escape de screen en C-x b, lo que significa que debes pulsar C-x seguido de b para enviar comandos a screen.

    caption always "%{= wb} %{= kG} %H %{-} %{= wk} %?%-Lw%?%{= bW}%n*%f %t%{-}%+Lw %=%{= kG} %D %M %d %Y %c": establece el formato de la línea de título de la ventana de screen.

Estos son algunos de los comandos más comunes que puedes incluir en un archivo screenrc, pero hay muchos más que puedes utilizar para personalizar la configuración de screen. Puedes consultar la documentación de screen para obtener más información sobre las opciones de configuración disponibles.