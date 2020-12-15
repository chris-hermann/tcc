#Este script serve como uma base de parametros necessários para as equações utilizadas na aplicação
#
#
#
#

#Relações de transmissão para tratores, utilizado para obter a potência na tomada de potência

relacaoTransmissao = {'4x2Firme': 0.72,
					'4x2Arado': 0.67,		
					'4x2Gradeado':	0.55,		
					'4x2TDAFirme':	0.77,		
					'4x2TDAArado':	0.73,	
					'4x2TDAGradeado': 0.65,		
					'4x4Firme': 0.78,		
					'4x4Arado': 0.75,			
					'4x4Gradeado':	0.70
					}

Parametros = {
				'Aradodeaivecas': [652, 0, 5.1, 1, 0.7, 0.45, 40],
				'Aradodediscos': [2, 0.013, 3, 0.032, 7, 0.049],
				'Subsoladorponteirasimples': [226, 0, 1.8, 1, 0.7, 0.45, 50],
				'Subsoladorponteiracomasas': [294, 0, 2.4, 1, 0.7, 0.45, 50],
				'GradedediscosaçãoduplaemXTandemPrimeira': [309, 16, 0, 1, 0.88, 0.78, 50],
				'GradedediscosaçãoduplaemXTandemSegunda': [216, 11.2, 0, 1, 0.88, 0.78, 30],
				'GradedediscosaçãoduplaemVOffsetPrimeira': [364, 18.8, 0, 1, 0.88, 0.78, 50],
				'GradedediscosaçãoduplaemVOffsetsegunda': [254, 13.2, 0, 1, 0.88, 0.78, 30],
				'GradedediscosaçãosimplesPrimeira': [124, 6.4, 0, 1, 0.88, 0.78, 25],
				'GradedediscosaçãosimplesSegunda': [86, 4.5, 0, 1, 0.88, 0.78, 20],
				'CultivadordecampoPrimeira': [46, 2.8, 0, 1, 0.85, 0.65, 30],
				'CultivadordecampoSegunda': [32, 1.9, 0, 1, 0.85, 0.65, 25],
				'Sulcador': [],
				'Semeadoramontadasementesgraúdas': [500, 0, 0, 1, 1, 1, 25],
				'Semeadoradearrastosementesgraúdas': [900, 0, 0, 1, 1, 1, 25],
				'Semeadoradearrastoadubadorapulverizadorasementesgraúdas': [1550, 0, 0, 1, 1, 1, 25],
				'Semeadoramontadasementesmiúdas': [],
				'Semeadoradearrastosementesmiúdas': []
			}

Eficiencia = {
				'Aradodeaivecas': [70, 90, 5, 10, 0.29, 1.8],
				'Aradodediscos': [70, 90, 5, 10, 0.29, 1.8],	#OUTRA METODOLOGIA - MATERIAL DO PROFESSOR
				'Subsoladorponteirasimples': [226, 0, 1.8, 1, 0.7, 0.45, 50],
				'Subsoladorponteiracomasas': [294, 0, 2.4, 1, 0.7, 0.45, 50],
				'GradedediscosaçãoduplaemXTandemPrimeira': [70, 90, 6.5, 11, 0.18, 0.17],
				'GradedediscosaçãoduplaemXTandemSegunda': [70, 90, 6.5, 11, 0.18, 0.17],
				'GradedediscosaçãoduplaemVOffsetPrimeira': [70, 90, 6.5, 11, 0.18, 0.17],
				'GradedediscosaçãoduplaemVOffsetsegunda': [70, 90, 6.5, 11, 0.18, 0.17],
				'GradedediscosaçãosimplesPrimeira': [70, 90, 6.5, 11, 0.18, 0.17],
				'GradedediscosaçãosimplesSegunda': [70, 90, 6.5, 11, 0.18, 0.17],
				'CultivadordecampoPrimeira': [70, 90, 8, 13, 0.27, 1.4],
				'CultivadordecampoSegunda': [70, 90, 8, 13, 0.27, 1.4],
				'Sulcador': [],
				'Semeadoramontadasementesgraúdas': [50, 75, 6.5, 11, 0.32, 2.1],
				'Semeadoradearrastosementesgraúdas': [50, 75, 6.5, 11, 0.32, 2.1],
				'Semeadoradearrastoadubadorapulverizadorasementesgraúdas': [50, 75, 6.5, 11, 0.32, 2.1],
				'Semeadoramontadasementesmiúdas': [50, 75, 6.5, 11, 0.32, 2.1],
				'Semeadoradearrastosementesmiúdas': [50, 75, 6.5, 11, 0.32, 2.1]
			}
