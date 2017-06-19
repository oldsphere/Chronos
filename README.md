REPLANNING

The idea is to have the objects even more separated

TimeNotebook
    - Just read and write on the TimeNotebook

Timer
    - Count without end

Timeout
    - Count a specified time
    - must have a run and check method

DynamicLine
    - Shows the information
    - Must have a updateTimer method which works with both, Timer and Timeout


chronos
    + Read the arguments
    + Load the timeNotebook
    + Launch the specific object
    + Display the information
    + Writes on the notebook

It shall be something like:
    
    ```python
    nt = MyNotebook(ntPath)
    if args.timeout:
        timer = Timeout(args.timeout)
    else:
        timer = Timer()
    timer.run()

    while True:
        try:
            dynLine.updateTimer(timer)
        except KeyboardInterrupt:
            cmd = input('Timer interrupted, What to do next?\n').lower()

            # Small command board
            if cmd.startswith('q'):
                break
            elif cmd.startswith('a'):
                # Parse the timer and add the specified time
            elif cmd.startswith('s'):
                disableAlarm = True
            elif cmd.startswith('r'):
                continue
            elif cmd.startswith('h') or cmd == '?':
                printHelp()
            else:
                print('Unknown instruction')

        nt.update(timer)
    ´´´


#martes 03 enero 2017 - 00:36
For now a change on the conception of time recording is applied to both Timer
and Timeout. I had no time to check the modifications but I hope they work
without too much effort.
The idea is to capture all the interruptions and other events and generate a
TimeBlock object for each of those.
This TimeBlock has the initTime, the endTime and a status, being currently the
available status 'normal','interrupted' and 'overtime'
The Timer and Timeout objects are blind to the task and category of the system
for reusing purposes. Thus, their property TimeBlockCollection has method to
assing a meaningful task and category to all the block contained.

It is intended that these TimeBlock will help the further visualization of the
different elements
Additionally, the entire information of the TimeNotebook shall be modified to
capture these TimeBlocks. These will mean that the storing file would be more
difficult to process by a person. 
Thus, the note application must include values to evaluate all these
inconveniences.

For tomorrow, test the new Timer and Timeout objects and write the new
TimeNotebook method. With that it shall me usable and new features, such as the
capability of silent and add new time would be included.

# lun 16/01/2017  20:58:14
Improvement
    Data processing:

    (Day | Month | Week) resume:
        Last week: 
            Category          HH:MM
              - task1         HH:MM
              - task2         HH:MM
              ...
            Category2         HH:MM
              - task1         HH:MM

    Week graph (using matplotlib):

    List categories:
    Modify category:


#lun 16/01/2017  21:56:15
    How to call the resume option...

    ```bash
    chronos -r W (this week)
    chronos -r D (today)
    chronos -r M (this month)
    chronos -r Y (this year)

    chornos -r 2W (last two weeks)
    chronos -r W2 (show the week 2)
    chronos -r W-1 (show previous week)
    chronos -r W-3 (show the third past week)

    chronos -r D-1 (show me yesterday)
    chronos -r 2D  (show me two days)
    ´´´

En definitiva la fecha se tiene que poner como:

    <span> <scale> <offset>

Por ahora voy a dejar de lado el span. Me quedo con el offset para
hacerlo funcional.

Si el offset es positivo seleciona una fecha concreta. Si el offset es
negativo seleciona ina fecha relativa.


#mar 17/01/2017  00:18:02
La función date_parse está incluida en auxiliar y funciona correctamente.
Usando los criterios de definición de fechas establecidos en el punto anterior
devuelve dos fechas (inicial y final)

Lo que faltaría sería poder pasarle esta información a un método de
TimeNotebook que devuelva una lista con las tareas.

    [ {"Category":"Leissure" , "init":"11/11/2015", "end":"11/11/2015...",
    "ID":"23"},
    ...
    ]

De esto tengo que sacar el tiempo total empleado...

Me gustaría poder añadir además comentarios a las notas. Algo con lo que pueda
hacerse un reporte o descripción de que tipo de actividades has hecho o el
exito del mismo.
Esto puede llevar a tener que re-estructurar el archivo de notebook...


#mar 17/01/2017  09:24:45

Vale, para representar el resumen de tiempos tengo que agrupar los resultdos
por categorias.

    ```python
    {"category":"Leissure",
     "time":2030, #secs
     "tasks":[ { "label":"label_1", "time":10},
               { "label":"label_2", "time":20} ]
    }
    ´´´

#vie 20/01/2017  15:11:41
La última vez quedó incluido la función resume que presentaba un pequño resumen
de las actividades realizadas esa semana, día o mes con la sintaxis adecuada
para ello.

Lo que me gustaría implementar hoy:
    - Ver el tiempo total que no ha quedado registrado [OK]
    - Función autocompletar

La función autocompletar es un poco más coñazo de lo que pensaba... sobre todo
si quiero incluirlo dentro del entorno de bash como estaba pensando.

Parece que el módulo que estuve mirando sobre readline funciona buen, pero
tiene que ejecutarse dentro de python.

La otra alternativa es correr un módulo llamado argcomplete, pero no logro
hacerlo funcionar. Según parece para que la función autocomplete funciona es
necesario activar una serie de opciones en bash

# mié 22/02/2017  17:13:45
- Working for the inclusión of a plot of tasks -
The TimeNotebook shall be modified to filter the tasks contained in a
spciefied time spam. 
    
    TimeNotebook.py
    ```python
    def filter_tasks(self,init,end):
    ´´´

- On the plotter the tasks shall regrouped by days.
- The rectangle asigned to each tasks would depend on the number of days to
  consider on the plot. 
  The default ticker system would will spread the yaxis among all the days
  to consider, a margin of 2.5% of the total height shall be considered

