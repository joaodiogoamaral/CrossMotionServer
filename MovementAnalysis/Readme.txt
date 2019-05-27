
Joao Amaral 29/11/2018

No seu estado corrente o openpose pode ser executado de 2 diferentes maneiras:


	1 ) ./CrossMotionOP.sh --compare <PathToVideo1> <PathToVideo1>

	- Esta opção executa o openPose guardando o seu output em dois diretórios temporários através de um script de shell. Após a execução do OP, o script executa um script de python onde extrai as equações referentes ao movimento do joelho do lado referente ao plano de filmagem que for detetado. Seguidamente as posições Y segundo o tempo (frames) são exibidas num gráfico e finalmente é calculada a semelhança co-sinusoidal entre os dois vetores. 

	NOTA: Como a semelhança tem de ser calculada entre vetores da mesma dimensão, o vetor de menores dimensões é preenchido com zeros de forma a ter uma dimensão concordante.




	2 )  ./CrossMotionOP.sh --store <PathToVideo> <exercise> 


De notar ainda que o segundo está inacabado.