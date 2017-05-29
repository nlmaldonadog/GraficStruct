import sys
import pygame
import time
from pygame.locals import *
from math import floor
from antlr4 import *
from MyLanguageVisitor import MyLanguageVisitor
from MyLanguageLexer import MyLanguageLexer
from MyLanguageParser import MyLanguageParser

noError = True
negro = (0,0,0)
blanco = (255,255,255)
azul = (107,35,142)
rojo = (239,57,24)
amarillo = (255,255,0)
dimensionScreen = (1200,700)

pygame.init()
pygame.display.set_caption("Graficador de Estructuras")
ventana = pygame.display.set_mode(dimensionScreen)
pygame.display.set_caption("canvases")
#secciones
menuBar = ventana.subsurface((0,0,dimensionScreen[0],30))
menuBar.fill(negro)
canvas = ventana.subsurface((0,30,dimensionScreen[0],dimensionScreen[1]*3/5))
canvas.fill(blanco)
codigo = ventana.subsurface((0,dimensionScreen[1]*3/5 +30,dimensionScreen[0],dimensionScreen[1]*2/5 - 30))
codigo.fill(negro)
pygame.display.update()
#colecciones de pilas, colas y listas
PILAS = {}
COLAS = {}
LISTAS = {}
structures = [ 'stack', 'list', 'queue' ]

table = {}

#PARTE DE MOSTRAR EL CODIGO
input = open("input.txt","r")
fuente = pygame.font.SysFont("courier",18)
#renderizar el string directamente en la superficie codigo
renglones = []
indice = 0
for line in input.readlines():
	result = str()
	for c in line:
		if c == '\t':
			result += '    ';
		else:
			result += c
	renglones.append(fuente.render( "     "+result[0:len(result)-1] ,0 , blanco))

def pintarCodigo( limMenor , limMayor , renglon):
	j=0
	for i in range(limMenor,limMayor):
		codigo.blit(renglones[i],(0,j*18))
		if i == renglon:
			pygame.draw.rect(codigo , blanco , (0,j*18,codigo.get_width(),18) , 2)
		j+=1

def actualizarCodigo(renglon):
	#caben 14 renglones
	codigo.fill(negro)
	r = len(renglones)
	if r <= 14:
		for i in range(r):
			codigo.blit(renglones[i],(0,i*18))
			if i == renglon:
				pygame.draw.rect(codigo , blanco , (0,i*18,codigo.get_width(),18) , 2)
	else:
		j = 0
		if renglon-7 < 0:
			pintarCodigo(0,15,renglon)
		elif renglon+7 > r:
			pintarCodigo(r-14,r , renglon)
		else:
			pintarCodigo(renglon-7 , renglon+7 , renglon)
	pygame.display.update()
	time.sleep(1)

class Pila:
	def __init__(self,superficie):
		self.pila = []
		self.superficie = superficie
		self.dimensionCaja = (40,40)

	def pintar(self):
		self.superficie.fill(blanco)
		length = len(self.pila)
		letra = pygame.font.SysFont("Arial",10)
		#marco
		pygame.draw.line(self.superficie, azul , (5 , 15 ) , ( 5, self.superficie.get_height()-25)  , 3)
		pygame.draw.line(self.superficie, azul , (5,self.superficie.get_height()-25) ,(self.dimensionCaja[0]+15,self.superficie.get_height()-25),3)
		pygame.draw.line(self.superficie, azul , (self.dimensionCaja[0]+15 , 15) , (self.dimensionCaja[0]+15, self.superficie.get_height()-25)  , 3)
		#cambiar dimensiones de la caja
		if self.dimensionCaja[1] != 40 and (length)*self.dimensionCaja[1]+35 < self.superficie.get_height():
			self.dimensionCaja = (self.dimensionCaja[0],self.dimensionCaja[1]+3)
		if (length)*self.dimensionCaja[1]+35 >= self.superficie.get_height():
			self.dimensionCaja = (self.dimensionCaja[0],self.dimensionCaja[1]-3)
		dx = 10
		dy = self.superficie.get_height()-30-self.dimensionCaja[1]
		for caja in self.pila:
			r = pygame.draw.rect(self.superficie, negro , (dx,dy,self.dimensionCaja[0],self.dimensionCaja[1]),1)
			dy-=self.dimensionCaja[1]
			cont = letra.render(caja , 0 , negro )
			anchoLetra = cont.get_width()
			if anchoLetra<self.dimensionCaja[0]:
				self.superficie.blit( cont , ( r[0]+(self.dimensionCaja[0]-anchoLetra)/2 , r[1] + self.dimensionCaja[1]/4 ) )
		pygame.display.update()

	def put(self,text):
		self.pila.append(text)
		self.pintar()

	def take(self):
		if len(self.pila) > 0:
			self.pila.pop(0)
			self.pintar()
			return True
		else:
			self.errorTake()
			return False

	def errorTake(self):
		#marco
		pygame.draw.line(self.superficie, azul , (5 , 15 ) , ( 5, self.superficie.get_height()-25)  , 3)
		pygame.draw.line(self.superficie, azul , (5,self.superficie.get_height()-25) ,(self.dimensionCaja[0]+15,self.superficie.get_height()-25),3)
		pygame.draw.line(self.superficie, azul , (self.dimensionCaja[0]+15 , 15) , (self.dimensionCaja[0]+15, self.superficie.get_height()-25)  , 3)

		dx = 10
		dy = self.superficie.get_height()-20
		r = pygame.draw.rect(self.superficie, negro , (dx,dy,self.dimensionCaja[0],self.dimensionCaja[1]/3),1)
		cuadrito = self.superficie.subsurface((r[0], r[1], r[2], r[3]))
		cuadrito.fill(rojo)
		pygame.draw.line(self.superficie , negro , (r[0], r[1]) , (r[0]+r[2], r[1]+r[3]) , 2)
		pygame.draw.line(self.superficie , negro , (r[2]+r[0], r[1]) , (r[0], r[1]+r[3]) , 2)
		pygame.display.update()

	def leng( self ):
		return len( self.pila )

class Cola:
	def __init__(self,superficie):
		self.cola = []
		self.dimensionCaja = (40,40)
		self.superficie = superficie

	def pintar(self):
		self.superficie.fill(blanco)
		length = len(self.cola)
		letra = pygame.font.SysFont("Arial",10)
		#marco
		pygame.draw.line(self.superficie, azul , (15 , 5 ) , (self.superficie.get_width()-25, 5 ) , 3)
		pygame.draw.line(self.superficie, azul , (15 , self.dimensionCaja[1]+15 ) , ( self.superficie.get_width()- 25, self.dimensionCaja[1]+15 ) , 3)
		#si las dimensiones de todas las cajas se reducen
		if self.dimensionCaja[0] != 40 and (length)*self.dimensionCaja[0]+35 < self.superficie.get_width():
			self.dimensionCaja = (self.dimensionCaja[0]+3,self.dimensionCaja[1])
		#si las dimensiones de todas las cajas se pasan de las dimensiones de la ventana
		if (length)*self.dimensionCaja[0]+30 >= self.superficie.get_width():
			self.dimensionCaja = (self.dimensionCaja[0]-3,self.dimensionCaja[1])

		dx = self.superficie.get_width()-35-self.dimensionCaja[0]
		#print self.superficie.get_width()-base[0]-self.dimensionCaja[0] , self.superficie.get_width()
		dy = 10
		for caja in self.cola:
			r = pygame.draw.rect(self.superficie, negro , ( dx, dy, self.dimensionCaja[0] , self.dimensionCaja[1]),1)
			dx-=self.dimensionCaja[0]
			cont = letra.render(caja , 0 , negro )
			anchoLetra = cont.get_width()
			if anchoLetra<self.dimensionCaja[0]:
				self.superficie.blit( cont , ( r[0]+(self.dimensionCaja[0]-anchoLetra)/2 , r[1] + self.dimensionCaja[1]/4 ) )
		pygame.display.update()

	def put(self,text):
		self.cola.append(text)
		self.pintar()

	def errorTake(self):
		base = (60,10)
		self.superficie.fill(blanco)
		pygame.draw.line(self.superficie, azul , (15 , 5 ) , ( self.superficie.get_width()-25, 5 ) , 3)
		pygame.draw.line(self.superficie, azul , (15 , self.dimensionCaja[1]+15 ) , ( self.superficie.get_width()- 25, self.dimensionCaja[1]+15 ) , 3)
		dx = self.superficie.get_width()-60
		dy = 10
		r = pygame.draw.rect(self.superficie, negro , ( dx, dy, self.dimensionCaja[0] , self.dimensionCaja[1]),1)
		cuadrito = self.superficie.subsurface((r[0], r[1], r[2], r[3]))
		cuadrito.fill(rojo)
		pygame.draw.line(self.superficie , negro , (r[0], r[1]) , (r[0]+r[2], r[1]+r[3]) , 2)
		pygame.draw.line(self.superficie , negro , (r[2]+r[0], r[1]) , (r[0], r[1]+r[3]) , 2)
		pygame.display.update()

	def take(self):
		if len(self.cola) > 0:
			self.cola.take(0)
			self.pintar()
			return True
		else:
			self.errorPop()
			return False

	def leng( self ):
		return len( self.cola )

class Lista:
	def __init__(self,superficie):
		self.lista = []
		self.superficie = superficie
		self.dimensionCaja = (40,40)

	def pintar(self, color):
		self.superficie.fill(color)
		length = len(self.lista)
		letra = pygame.font.SysFont("Arial",10)
		#marco
		dx = 15
		dy = 0
		index = 0
		for caja in self.lista:
			#si ya se paso del limite derecho de la superficie
			if dx+self.dimensionCaja[0] > self.superficie.get_width():
				dy += 20+self.dimensionCaja[1]
				dx = 15
			r = pygame.draw.rect(self.superficie, negro , (dx,dy,self.dimensionCaja[0],self.dimensionCaja[1]),1)
			dx +=self.dimensionCaja[1]
			cont = letra.render(str(caja) , 0 , negro )
			anchoLetra = cont.get_width()
			idx = letra.render(str(index) , 0 ,negro)
			xt = idx.get_width()
			self.superficie.blit(idx , ( (dx-40)+(40-xt)/2  , r[3]+dy ) )
			index += 1
			if anchoLetra<self.dimensionCaja[0]:
				self.superficie.blit( cont , ( r[0]+(self.dimensionCaja[0]-anchoLetra)/2 , r[1] + self.dimensionCaja[1]/4 ) )
		pygame.display.update()

	def add(self,index,texto):
		self.lista.insert(index,texto)
		self.pintar(amarillo)

	def remove(self , index):
		if index > 0 and index < len(self.lista)-1:
			self.cola.pop(index)
			self.pintar(amarillo)
			return True
		else:
			self.errorRemove()
			return False

	def errorRemove(self):
		self.pintar(rojo)

	def leng( self ):
		return len( self.lista )

def newLista(name):
	numListas = len(LISTAS)
	x = len(PILAS)*60
	y = len(COLAS)*60+20
	dx = canvas.get_width()-x
	dy = canvas.get_height()-y if numListas == 0 else (canvas.get_height()/numListas)-y
	canvasLista = canvas.subsurface(x,y,dx,dy)
	letra = pygame.font.SysFont("Arial",18,False,True)
	nameLista = letra.render(name , 0 , negro)
	canvasLista.fill(amarillo)
	canvas.blit(nameLista , ( (dx-x)/2 , y-20 ) )
	LISTAS[name]=[ Lista(canvasLista) , numListas ]
	pygame.display.update()

def reorganizarListas():
	numListas = len(LISTAS)
	x = len(PILAS)*60
	y = len(COLAS)*60
	dy = canvas.get_height()-y if numListas == 0 else (canvas.get_height()-y)/numListas
	for lista in LISTAS:
		index = LISTAS[lista][1]
		nuevoCanvas = canvas.subsurface( x , y + 20 + dy*index , canvas.get_width()-x , dy - 20 )
		nuevaLista = Lista(nuevoCanvas)
		nuevaLista.lista = LISTAS[lista][0].lista
		LISTAS[lista][0]=nuevaLista
		LISTAS[lista][0].pintar(blanco)
	pygame.display.update()

def newCola(name):
	print name
	numPilas = len(PILAS)*60
	anchura = canvas.get_width()-numPilas-40
	altura = 60
	numColas = len(COLAS)
	canvasCola = canvas.subsurface(numPilas,numColas*60 , anchura, altura)
	letra = pygame.font.SysFont("Arial",20)
	nameCola = letra.render(name , 0 ,negro)
	texto = pygame.transform.rotate(nameCola, 270)
	canvas.blit(texto ,  (anchura, numColas*60 +10))
	canvasCola.fill(amarillo)
	COLAS[name]=[Cola(canvasCola), numColas]
	reorganizarListas()
	pygame.display.update()

def reorganizarColas():
	numPilas = len(PILAS)*60
	anchura = canvas.get_width()-numPilas-40
	altura = 60
	for cola in COLAS:
		index = COLAS[cola][1]
		nuevoCanvas = canvas.subsurface(numPilas,index*60,anchura,altura)
		nuevaCola = Cola(nuevoCanvas)
		nuevaCola.cola = COLAS[cola][0].cola
		COLAS[cola][0]=nuevaCola
		COLAS[cola][0].pintar()
	pygame.display.update()

def newPila(name):
	num = len(PILAS)
	altura = canvas.get_height()-40
	anchura = 60

	canvasPila = canvas.subsurface(num*60,0,anchura,altura)
	letra = pygame.font.SysFont("Arial",18,False,True)
	namePila = letra.render(name , 0 ,negro)
	canvas.blit(namePila , ( (anchura - namePila.get_width())/2 + num*60 , altura ) )
	canvasPila.fill(rojo)
	PILAS[name] = Pila(canvasPila)
	reorganizarColas()
	reorganizarListas()
	pygame.display.update()

def abs( a ):
	return False if a < 0 else True

class MyVisitor(MyLanguageVisitor):

	def visitCommands(self, ctx):
		return self.visitChildren(ctx)

	def visitCommand(self, ctx):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by MyLanguageParser#declaration.
	def visitDeclaration(self, ctx):
		name = ctx.ID().getText()
		if table.get( name ) != None:
			line = ctx.ID().getSymbol().line
			col = ctx.ID().getSymbol().column
			print "<" + str( line ) + ", " + str( col ) + ">Error Semantico, la variable con nombre: \"" + name + "\" ya fue declarada.\n"
			sys.exit()
		else:
			if ctx.VAR() != None:
				table[ name ] = self.visitExpr( ctx.expr() )
			else:
				table[ name ] = ctx.STRUCTS().getText()
				if ctx.STRUCTS().getText() == 'stack':
					newPila( name )
					actualizarCodigo(ctx.STRUCTS().getSymbol().line - 1)
				elif ctx.STRUCTS().getText() == 'queue':
					newCola( name )
					actualizarCodigo(ctx.STRUCTS().getSymbol().line - 1)
				elif ctx.STRUCTS().getText() == 'list':
					newLista( name )
					actualizarCodigo(ctx.STRUCTS().getSymbol().line - 1)
		pass

	def visitMethod(self, ctx):
		if ctx.ID() != None:
			name = ctx.ID().getText()
			if name not in table:
				if table[ name ] not in structures:
					line = ctx.ID().getSymbol().line
					col = ctx.ID().getSymbol().column
					print "<" + str( line ) + ", " + str( col ) + ">Error Semantico, la variable con nombre: \"" + name + "\" no fue declarada.\n"
					sys.exit()
					return None
				else:
					line = ctx.ID().getSymbol().line
					col = ctx.ID().getSymbol().column
					print "<" + str( line ) + ", " + str( col ) + ">Error Semantico, la variable con nombre: \"" + name + "\" no es una estructura.\n"
					sys.exit()
					return None
			else:
				if ctx.methods().var() != None:
					if ctx.methods().var().MTD() != None:
						actualizarCodigo(ctx.methods().var().MTD().getSymbol().line - 1)
						if table[ name ] == 'queue':
							return COLAS[ name ][ 0 ].leng()
						elif table[ name ] == 'stack':
							return PILAS[ name ].leng()
						elif table[ name ] == 'list':
							return LISTAS[ name ][ 0 ].leng()
					elif ctx.methods().var().TAK() != None:
						if table[ name ] == 'queue':
							thing = COLAS[ name ][ 0 ].take()
						elif table[ name ] == 'stack':
							thing = PILAS[ name ].take()
						else:
							line = ctx.methods().var().TAK().getSymbol().line
							col = ctx.methods().var().TAK().getSymbol().column
							print "<" + str( line ) + ", " + str( col ) + ">Error Semantico, la variable con nombre: \"" + name + "\" no es una cola ni pila.\n"
							sys.exit()
							return None
						if thing:
							actualizarCodigo(ctx.methods().var().TAK().getSymbol().line - 1)
							return thing
						else:
							line = ctx.methods().var().TAK().getSymbol().line
							col = ctx.methods().var().TAK().getSymbol().column
							print "<" + str( line ) + ", " + str( col ) + ">Error Semantico, la estructura con nombre: \"" + name + "\" no cuenta con elementos.\n"
							sys.exit()
							return None
				elif ctx.methods().vardos() != None:
					if ctx.methods().vardos().MTH() != None:
						if table[ name ] == 'queue':
							COLAS[ name ][ 0 ].put( str( ctx.methods().expr() ) )
						elif table[ name ] == 'stack':
							PILAS[ name ].put( str( ctx.methods().expr() ) )
						else:
							line = ctx.methods().vardos().MTH().getSymbol().line
							col = ctx.methods().vardos().MTH().getSymbol().column
							print "<" + str( line ) + ", " + str( col ) + ">Error Semantico, la variable con nombre: \"" + name + "\" no es una cola ni pila.\n"
							sys.exit()
							return None
						actualizarCodigo(ctx.methods().vardos().MTH().getSymbol().line - 1)
					elif ctx.methods().vardos().REM() != None:
						if table[ name ] == 'list':
							LISTAS[ name ][ 0 ].remove( ctx.methods().expr() )
						else:
							line = ctx.methods().vardos().MTH().getSymbol().line
							col = ctx.methods().vardos().MTH().getSymbol().column
							print "<" + str( line ) + ", " + str( col ) + ">Error Semantico, la variable con nombre: \"" + name + "\" no es una lista.\n"
							sys.exit()
							return None
						actualizarCodigo(ctx.methods().vardos().REM().getSymbol().line - 1)
				else:
					if table[ name ] == 'list':
						num1 = int( self.visitExpr( ctx.methods().expr( 0 ) ) )
						num2 = float( self.visitExpr( ctx.methods().expr( 1 ) ) )
						LISTAS[ name ][ 0 ].add( num1, str( num2 ) )
					else:
						line = ctx.methods().METHOD().getSymbol().line
						col = ctx.methods().METHOD().getSymbol().column
						print "<" + str( line ) + ", " + str( col ) + ">Error Semantico, la variable con nombre: \"" + name + "\" no es una lista.\n"
						sys.exit()
						return None
					actualizarCodigo(ctx.methods().METHOD().getSymbol().line - 1)
		return None

	def visitMethods(self, ctx):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by MyLanguageParser#var.
	def visitVar(self, ctx):
		return self.visitChildren(ctx)

	# Visit a parse tree produced by MyLanguageParser#vardos.
	def visitVardos(self, ctx):
		return self.visitChildren(ctx)

	def visitConditional(self, ctx):
		op = ctx.ROP().getText()
		num1 = float( self.visitExpr( ctx.expr( 0 ) ) )
		num2 = float( self.visitExpr( ctx.expr( 1 ) ) )
		ans = None
		if op == "<":
			ans = num1 < num2
		elif op == "<=":
			ans = num1 <= num2
		elif op == ">":
			ans = num1 > num2
		elif op == ">=":
			ans = num1 >= num2
		elif op == "==":
			ans = abs( num1-num2 ) < 0.000000001
		elif op == "!=":
			ans = abs( num1-num2 ) > 0.000000001
		if ans:
			self.visitCommands( ctx.commands() )
			return None
		return self.visitPostcond( ctx.postcond() )

	def visitPostcond(self, ctx):
		if ctx.ELSEIF() != None:
			op = ctx.ROP().getText();
			num1 = float( self.visitExpr( ctx.expr( 0 ) ) )
			num2 = float( self.visitExpr( ctx.expr( 1 ) ) )
			ans = None
			if op == "<":
				ans = num1 < num2
			elif op == "<=":
				ans = num1 <= num2
			elif op == ">":
				ans = num1 > num2
			elif op == ">=":
				ans = num1 >= num2
			elif op == "==":
				ans = abs( num1-num2 ) < 0.000000001
			elif op == "!=":
				ans = abs( num1-num2 ) > 0.000000001
			if ans:
				self.visitCommands(ctx.commands())
				return None
			return self.visitPostcond(ctx.postcond())
		elif ctx.ELSE() != None:
			self.visitCommands(ctx.commands())
		return None

	def visitRepeat(self, ctx):
		times = int( float( self.visitExpr( ctx.expr() ) ) )
		for i in range( times ):
			self.visitCommands(ctx.commands());
		return None

	def visitPrintexpr(self, ctx):
		return self.visitChildren(ctx)

	def visitPrintwhat(self, ctx):
		if ctx.expr() != None:
			ans = float( self.visitExpr( ctx.expr() ) )
			aux = int( floor( ans ) )
			if ans - aux < 1e-9:
				print aux
			else:
				print ans
		else:
			print self.visitMethod( ctx.method() )
		return None

	def visitExpr(self, ctx):
		if ctx.DOUBLE() != None:
			num = float( ctx.DOUBLE().getText() )
			return num
		elif ctx.PIZQ() != None:
			return self.visitExpr( ctx.expr(0) )
		elif ctx.ID() != None:
			name = ctx.ID().getText()
			if name not in table:
				line = ctx.ID().getSymbol().line
				col = ctx.ID().getSymbol().column
				print "<" + str( line ) + ", " + str( col ) + ">Error Semantico, la variable con nombre: \"" + name + "\" no fue declarada.\n"
				sys.exit()
				return None
			else:
				return table[ name ]
		else:
			op = ctx.MULOP().getText() if ctx.MULOP() != None else ctx.SUMOP().getText()
			num1 = float( self.visitExpr( ctx.expr(0) ) )
			num2 = float( self.visitExpr( ctx.expr(1) ) )
			ans = None
			if op == "+":
				ans = num1 + num2
			elif op == "-":
				ans = num1 - num2
			elif op == "*":
				ans = num1 * num2
			elif op == "/":
				ans = num1 / num2
			return ans

def main(argv):
	input = FileStream(argv[1])
	lexer = MyLanguageLexer(input)
	stream = CommonTokenStream(lexer)
	parser = MyLanguageParser(stream)
	tree = parser.commands()
	loader = MyVisitor()
	loader.visit( tree )
	print COLAS, PILAS, LISTAS
	while True:
		for evento in pygame.event.get():
			if evento.type == QUIT:
				pygame.quit()
				sys.exit()

if __name__ == '__main__':
	main(sys.argv)
