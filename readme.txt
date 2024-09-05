A abertura do arquivo 'trabalho.py' deve ser realizado no diretório do arquivo da seguinte forma:

python trabalho.py nome_arquivo_memoria endereco_primeira_instrucao tamanho_vetor

Os argumentos são:
1- nome_arquivo_memoria
Nome do arquivo que simulará a memória do computador, o qual deve estar no mesmo diretório do arquivo python.

2- endereco_primeira_instrucao
Endereço da primeira instrução na memória, informado em hexadecimal (Exemplo: 0xFF).

3- tamanho_vetor
Indica o tamanho do vetor presente na memória caso algum algoritmo utilize vetores. Por padrão, o vetor sempre estará alocado a partir de 0x00,
ocupando as n-1 posições a seguir, de forma consecutiva (0x00, 0x01, 0x02...), sendo n o tamanho do vetor.

A execução do trabalho resultará em um novo arquivo chamado memoria_ajustada.ias no qual ocorrerá o processamento dos dados e execução das
instruções, pois, dessa forma, é possível observar os dados no arquivo original antes da execução do programa e os dados no arquivo gerado
após a execução do programa. Além disso, o processo de criação do novo arquivo é responsável por formatar a memória, de forma que cada endereço
ocupa de fato um número fixo de espaços (tamanho da memória é fixo para todos os endereços, o qual é indicado por uma constante em 'trabalho.py'),
permitindo maior liberdade no momento de escrever a memória - comentários podem ser realizados de forma afastada.

Entre a execução de cada instrução, os valores de cada registrador são exibidos e é necessário apertar [ENTER] para que o algoritmo prossiga.

O acesso ao vetor é realizado ao utilizar asteriscos para indicar o endereço que possui o índice. Por exemplo, se o endereço 0x17 possuir o número 1
como dado, a instrução LOAD_M *0x17* acessará o índice 1 do vetor (ou seja, como todo vetor começa em 0x00, o índice 1 do vetor é referente ao endereço
0x01, sendo o dado que está nesse endereço o carregado no acumulador após a instrução).

Os algoritmos desenvolvidos são:

1- fibonacci.ias
python trabalho.py fibonacci.ias 0x05 0

Esse arquivo de memória possui as instruções começando no endereço 0x05, as quais desenvolvem um algoritmo que fornece o n-ésimo termo da
Sequência de Fibonacci, sendo que n está disposto no primeiro endereço de memória (0x00). O elemento fornecido pelo código será sempre o
inteiro presente no último endereço ocupado pelos dados, normalmente estando em 0x03 ou 0x04 (depende do tamanho de n).
O argumento relativo ao tamanho do vetor não será utilizado por esse algoritmo, pois não há vetor na memória que seja utilizado.

O arquivo em questão que está sendo enviado possui n = 7, dispondo o dado 13 no endereço 0x04 após a execução do algoritmo, o qual corresponde
ao sétimo termo da Sequência.

2- selection_sort.ias
python trabalho.py selection_sort.ias 0x1D 10

Esse arquivo de memória possui as intruções começando no endereço 0x1D, as quais desenvolvem um algoritmo que ordena o vetor disposto na memória
utilizando o método de Selection Sort. O endereço 0x0D guarda o tamanho de vetor e é utilizado como um contador; o endereço 0x0E guarda o índice
do início da parte desordenada; o endereço 0x0F guarda um contador para analisar cada índice do vetor; os endereços 0x10 e 0x11 guardam os valores
que são comparados, enquanto os endereços 0x13 e 0x14 guardam seus respectivos índices no vetor; por fim, o endereço 0x12 é um espaço de memória
auxiliar, utilizado no momento de trocar os elementos de posição. Comentários foram escritos na memória para indicar os locais em que os dados e as
rotinas são guardadas, os quais são resolvidos após a formatação da memória.
O argumento relativo ao tamanho do vetor deve ser correspondente àquele disposto na memória (endereço 0x0D) para que o vetor disposto seja ordenado
de forma apropriada. Todos os números no vetor devem ser positivos e ele tem tamanho máximo de 13, podendo ser modificado (mantendo as dadas restrições).

O arquivo em questão que está sendo enviado possui um vetor de tamanho 10, com elementos que estão dispostos de forma desordenada. Após a execução do
algoritmo, todo o vetor estará ordenado.