## script for converting Jason's gTrains into Neuron gTrains
## This version does currently not use arrays

i = 0


while i <= 0:

    nS_filename = "E:/neuroConstruct/models/Dan_GranCell/gTrains_nS/gAMPA_" + str(i) + ".txt"
    Neuron_filename = "E:/neuroConstruct/models/Dan_GranCell/gAMPA_" + str(i) + ".txt"
    gTrains_nS = open(nS_filename, 'r')
    gTrains_Neuron = open(Neuron_filename, 'w')


    for line in gTrains_nS:
        nS_value = float(line)
        final_value = float(nS_value) * 100000 / (1000000 * 314.15927)
        print "--- %s converted to: %s"%(nS_value, final_value)

        gTrains_Neuron.write(str(final_value)+"\n")

    print "Done"

    i = i + 1
    gTrains_nS.close()
    gTrains_Neuron.close()


    #Version with arrays

    #nS = gTrains_nS.readlines()
    #Neuron = []

    #for item in nS:
    #    final_value = float(item) * 100000 / (1000000 * 314.15927)
    #    Neuron.append(str(final_value))

    #for item in Neuron:
    #    string = item + "\n"
    #    gTrains_Neuron.write(string)
    #i = i + 1
    #gTrains_nS.close()
    #gTrains_Neuron.close()



