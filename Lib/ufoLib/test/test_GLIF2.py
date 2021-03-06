from __future__ import unicode_literals
import unittest
from ufoLib.glifLib import GlifLibError, readGlyphFromString, writeGlyphToString
from ufoLib.test.testSupport import Glyph, stripText

try:
	basestring
except NameError:
	basestring = str
# ----------
# Test Cases
# ----------

class TestGLIF2(unittest.TestCase):

	def assertEqual(self, first, second, msg=None):
		if isinstance(first, basestring):
			first = stripText(first)
		if isinstance(second, basestring):
			second = stripText(second)
		return super(TestGLIF2, self).assertEqual(first, second, msg=msg)

	def pyToGLIF(self, py):
		py = stripText(py)
		glyph = Glyph()
		exec(py, {"glyph" : glyph, "pointPen" : glyph})
		glif = writeGlyphToString(glyph.name, glyphObject=glyph, drawPointsFunc=glyph.drawPoints, formatVersion=2)
		glif = "\n".join(glif.splitlines()[1:])
		return glif

	def glifToPy(self, glif):
		glif = stripText(glif)
		glif = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + glif
		glyph = Glyph()
		readGlyphFromString(glif, glyphObject=glyph, pointPen=glyph)
		return glyph.py()

	def testTopElement(self):
		# not glyph
		glif = """
		<notglyph name="a" format="2">
			<outline>
			</outline>
		</notglyph>
		"""
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testName(self):
		# legal
		glif = """
		<glyph name="a" format="2">
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# empty
		glif = """
		<glyph name="" format="2">
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = ""
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# not a string
		py = """
		glyph.name = 1
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)

	def testFormat(self):
		# legal
		glif = """
		<glyph name="a" format="2">
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# wrong number
		glif = """
		<glyph name="a" format="-1">
			<outline>
			</outline>
		</glyph>
		"""
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# not an int
		glif = """
		<glyph name="a" format="A">
			<outline>
			</outline>
		</glyph>
		"""
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testBogusGlyphStructure(self):
		# unknown element
		glif = """
		<glyph name="a" format="2">
			<unknown />
		</glyph>
		"""
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# content
		glif = """
		<glyph name="a" format="2">
			Hello World.
		</glyph>
		"""
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testAdvance(self):
		# legal: width and height
		glif = """
		<glyph name="a" format="2">
			<advance height="200" width="100"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.width = 100
		glyph.height = 200
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: width and height floats
		glif = """
		<glyph name="a" format="2">
			<advance height="200.1" width="100.1"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.width = 100.1
		glyph.height = 200.1
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: width
		glif = """
		<glyph name="a" format="2">
			<advance width="100"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.width = 100
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: height
		glif = """
		<glyph name="a" format="2">
			<advance height="200"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.height = 200
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# illegal: not a number
		glif = """
		<glyph name="a" format="2">
			<advance width="a"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.width = "a"
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		glif = """
		<glyph name="a" format="2">
			<advance height="a"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.height = "a"
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testUnicodes(self):
		# legal
		glif = """
		<glyph name="a" format="2">
			<unicode hex="0061"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.unicodes = [97]
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		glif = """
		<glyph name="a" format="2">
			<unicode hex="0062"/>
			<unicode hex="0063"/>
			<unicode hex="0061"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.unicodes = [98, 99, 97]
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# illegal
		glif = """
		<glyph name="a" format="2">
			<unicode hex="1.1"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "zzzzzz"
		glyph.unicodes = ["1.1"]
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testNote(self):
		glif = """
		<glyph name="a" format="2">
			<note>
				hello
			</note>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.note = "hello"
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)

	def testLib(self):
		glif = """
		<glyph name="a" format="2">
			<outline>
			</outline>
			<lib>
				<dict>
					<key>dict</key>
					<dict>
						<key>hello</key>
						<string>world</string>
					</dict>
					<key>float</key>
					<real>2.5</real>
					<key>int</key>
					<integer>1</integer>
					<key>list</key>
					<array>
						<string>a</string>
						<string>b</string>
						<integer>1</integer>
						<real>2.5</real>
					</array>
					<key>string</key>
					<string>a</string>
				</dict>
			</lib>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.lib = {"dict" : {"hello" : "world"}, "float" : 2.5, "int" : 1, "list" : ["a", "b", 1, 2.5], "string" : "a"}
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)

	def testGuidelines(self):
		# legal
		glif = """
		<glyph name="a" format="2">
			<guideline x="1"/>
			<guideline y="1"/>
			<guideline x="1" y="1" angle="0"/>
			<guideline x="1" y="1" angle="360"/>
			<guideline x="1.1" y="1.1" angle="45.5"/>
			<guideline x="1" name="a"/>
			<guideline x="1" color="1,1,1,1"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"x" : 1}, {"y" : 1}, {"angle" : 0, "x" : 1, "y" : 1}, {"angle" : 360, "x" : 1, "y" : 1}, {"angle" : 45.5, "x" : 1.1, "y" : 1.1}, {"name" : "a", "x" : 1}, {"color" : "1,1,1,1", "x" : 1}]
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# x not an int or float
		glif = """
		<glyph name="a" format="2">
			<guideline x="a" y="1" angle="45"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"angle" : 45, "x" : "a", "y" : 1}]
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# y not an int or float
		glif = """
		<glyph name="a" format="2">
			<guideline x="1" y="y" angle="45"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"angle" : 45, "x" : 1, "y" : "a"}]
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# angle not an int or float
		glif = """
		<glyph name="a" format="2">
			<guideline x="1" y="1" angle="a"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"angle" : "a", "x" : 1, "y" : 1}]
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# x missing
		glif = """
		<glyph name="a" format="2">
			<guideline y="1" angle="45"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"angle" : 45, "y" : 1}]
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# y missing
		glif = """
		<glyph name="a" format="2">
			<guideline x="1" angle="45"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"angle" : 45, "x" : 1}]
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# angle missing
		glif = """
		<glyph name="a" format="2">
			<guideline x="1" y="1"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"x" : 1, "y" : 1}]
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# angle out of range
		glif = """
		<glyph name="a" format="2">
			<guideline x="1" y="1" angle="-1"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"angle" : -1, "x" : "1", "y" : 1}]
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		glif = """
		<glyph name="a" format="2">
			<guideline x="1" y="1" angle="361"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"angle" : 361, "x" : "1", "y" : 1}]
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testAnchors(self):
		# legal
		glif = """
		<glyph name="a" format="2">
			<anchor x="1" y="2" name="test" color="1,0,0,1"/>
			<anchor x="1" y="2"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.anchors = [{"color" : "1,0,0,1", "name" : "test", "x" : 1, "y" : 2}, {"x" : 1, "y" : 2}]
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# x not an int or float
		glif = """
		<glyph name="a" format="2">
			<anchor x="a" y="1"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.anchors = [{"x" : "a", "y" : 1}]
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# y not an int or float
		glif = """
		<glyph name="a" format="2">
			<anchor x="1" y="a"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.anchors = [{"x" : 1, "y" : "a"}]
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# x missing
		glif = """
		<glyph name="a" format="2">
			<anchor y="1"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.anchors = [{"y" : 1}]
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# y missing
		glif = """
		<glyph name="a" format="2">
			<anchor x="1"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.anchors = [{"x" : 1}]
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testImage(self):
		# legal
		glif = """
		<glyph name="a" format="2">
			<image fileName="test.png" xScale="2" xyScale="3" yxScale="6" yScale="5" xOffset="1" yOffset="4" color="1,1,1,1"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.image = {"color" : "1,1,1,1", "fileName" : "test.png", "xOffset" : 1, "xScale" : 2, "xyScale" : 3, "yOffset" : 4, "yScale" : 5, "yxScale" : 6}
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: no color or transformation
		glif = """
		<glyph name="a" format="2">
			<image fileName="test.png"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.image = {"fileName" : "test.png", "xOffset" : 0, "xScale" : 1, "xyScale" : 0, "yOffset" : 0, "yScale" : 1, "yxScale" : 0}
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# no file name
		glif = """
		<glyph name="a" format="2">
			<image xScale="2" xyScale="3" yxScale="6" yScale="5" xOffset="1" yOffset="4" color="1,1,1,1"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.image = {"color" : "1,1,1,1", "xOffset" : 1, "xScale" : 2, "xyScale" : 3, "yOffset" : 4, "yScale" : 5, "yxScale" : 6}
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# bogus transformation
		glif = """
		<glyph name="a" format="2">
			<image fileName="test.png" xScale="a" xyScale="3" yxScale="6" yScale="5" xOffset="1" yOffset="4"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.image = {"fileName" : "test.png", "xOffset" : 1, "xScale" : "a", "xyScale" : 3, "yOffset" : 4, "yScale" : 5, "yxScale" : 6}
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		glif = """
		<glyph name="a" format="2">
			<image fileName="test.png" xScale="2" xyScale="a" yxScale="6" yScale="5" xOffset="1" yOffset="4"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.image = {"fileName" : "test.png", "xOffset" : 1, "xScale" : 2, "xyScale" : "a", "yOffset" : 4, "yScale" : 5, "yxScale" : 6}
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		glif = """
		<glyph name="a" format="2">
			<image fileName="test.png" xScale="2" xyScale="3" yxScale="a" yScale="5" xOffset="1" yOffset="4"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.image = {"fileName" : "test.png", "xOffset" : 1, "xScale" : 2, "xyScale" : 3, "yOffset" : 4, "yScale" : 5, "yxScale" : "a"}
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		glif = """
		<glyph name="a" format="2">
			<image fileName="test.png" xScale="2" xyScale="3" yxScale="6" yScale="a" xOffset="1" yOffset="4"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.image = {"fileName" : "test.png", "xOffset" : 1, "xScale" : 2, "xyScale" : 3, "yOffset" : 4, "yScale" : "a", "yxScale" : 6}
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		glif = """
		<glyph name="a" format="2">
			<image fileName="test.png" xScale="2" xyScale="3" yxScale="6" yScale="5" xOffset="a" yOffset="4"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.image = {"fileName" : "test.png", "xOffset" : "a", "xScale" : 2, "xyScale" : 3, "yOffset" : 4, "yScale" : 5, "yxScale" : 6}
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		glif = """
		<glyph name="a" format="2">
			<image fileName="test.png" xScale="2" xyScale="3" yxScale="6" yScale="5" xOffset="1" yOffset="a"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.image = {"fileName" : "test.png", "xOffset" : 1, "xScale" : 2, "xyScale" : 3, "yOffset" : "a", "yScale" : 5, "yxScale" : 6}
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# bogus color
		glif = """
		<glyph name="a" format="2">
			<image fileName="test.png" color="1,1,1,x"/>
			<outline>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.image = {"color" : "1,1,1,x"}
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testOutline(self):
		# unknown element
		glif = """
		<glyph name="a" format="2">
			<outline>
				<unknown/>
			</outline>
		</glyph>
		"""
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# content
		glif = """
		<glyph name="a" format="2">
			<outline>
				hello
			</outline>
		</glyph>
		"""
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testComponent(self):
		# legal
		glif = """
		<glyph name="a" format="2">
			<outline>
				<component base="x" xScale="2" xyScale="3" yxScale="6" yScale="5" xOffset="1" yOffset="4"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.addComponent(*["x", (2, 3, 6, 5, 1, 4)])
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# no base
		glif = """
		<glyph name="a" format="2">
			<outline>
				<component xScale="2" xyScale="3" yxScale="6" yScale="5" xOffset="1" yOffset="4"/>
			</outline>
		</glyph>
		"""
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# bogus values in transformation
		glif = """
		<glyph name="a" format="2">
			<outline>
				<component base="x" xScale="a" xyScale="3" yxScale="6" yScale="5" xOffset="1" yOffset="4"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.addComponent(*["x", ("a", 3, 6, 5, 1, 4)])
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		glif = """
		<glyph name="a" format="2">
			<outline>
				<component base="x" xScale="a" xyScale="3" yxScale="6" yScale="5" xOffset="1" yOffset="4"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.addComponent(*["x", (2, "a", 6, 5, 1, 4)])
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		glif = """
		<glyph name="a" format="2">
			<outline>
				<component base="x" xScale="2" xyScale="3" yxScale="a" yScale="5" xOffset="1" yOffset="4"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.addComponent(*["x", (2, 3, "a", 5, 1, 4)])
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		glif = """
		<glyph name="a" format="2">
			<outline>
				<component base="x" xScale="2" xyScale="3" yxScale="6" yScale="a" xOffset="1" yOffset="4"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.addComponent(*["x", (2, 3, 6, "a", 1, 4)])
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		glif = """
		<glyph name="a" format="2">
			<outline>
				<component base="x" xScale="2" xyScale="3" yxScale="6" yScale="5" xOffset="a" yOffset="4"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.addComponent(*["x", (2, 3, 6, 5, "a", 4)])
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		glif = """
		<glyph name="a" format="2">
			<outline>
				<component base="x" xScale="2" xyScale="3" yxScale="6" yScale="5" xOffset="1" yOffset="a"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.addComponent(*["x", (2, 3, 6, 5, 1, "a")])
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testContour(self):
		# legal: one contour
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: two contours
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="1" y="2" type="move"/>
				</contour>
				<contour>
					<point x="1" y="2" type="move"/>
					<point x="10" y="20" type="line"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(1, 2)], **{"segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath()
		pointPen.addPoint(*[(1, 2)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(10, 20)], **{"segmentType" : "line", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# unknown element
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<unknown/>
				</contour>
			</outline>
		</glyph>
		"""
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testContourIdentifier(self):
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour identifier="foo">
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath(**{"identifier" : "foo"})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)

	def testPointCoordinates(self):
		# legal: int
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="1" y="-2" type="move"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(1, -2)], **{"segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: float
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="1.1" y="-2.2" type="move"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(1.1, -2.2)], **{"segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: int
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="a" y="2" type="move"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[("a", 2)], **{"segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# legal: int
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="1" y="a" type="move"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(1, "a")], **{"segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testPointTypeMove(self):
		# legal
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="1" y="-2" type="move"/>
					<point x="3" y="-4" type="line"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(1, -2)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(3, -4)], **{"segmentType" : "line", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: smooth=True
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="1" y="-2" type="move" smooth="yes"/>
					<point x="3" y="-4" type="line"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(1, -2)], **{"segmentType" : "move", "smooth" : True})
		pointPen.addPoint(*[(3, -4)], **{"segmentType" : "line", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# illegal: not at start
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="3" y="-4" type="line"/>
					<point x="1" y="-2" type="move"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(3, -4)], **{"segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testPointTypeLine(self):
		# legal
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="1" y="-2" type="move"/>
					<point x="3" y="-4" type="line"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(1, -2)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(3, -4)], **{"segmentType" : "line", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: start of contour
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="1" y="-2" type="line"/>
					<point x="3" y="-4" type="line"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(1, -2)], **{"segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(3, -4)], **{"segmentType" : "line", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: smooth=True
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="1" y="-2" type="move"/>
					<point x="3" y="-4" type="line" smooth="yes"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(1, -2)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(3, -4)], **{"segmentType" : "line", "smooth" : True})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)

	def testPointTypeCurve(self):
		# legal
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="0" type="move"/>
					<point x="0" y="65"/>
					<point x="65" y="200"/>
					<point x="100" y="200" type="curve"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 0)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(0, 65)], **{"smooth" : False})
		pointPen.addPoint(*[(65, 200)], **{"smooth" : False})
		pointPen.addPoint(*[(100, 200)], **{"segmentType" : "curve", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: start of contour
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="100" y="200" type="curve"/>
					<point x="0" y="65"/>
					<point x="65" y="200"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(100, 200)], **{"segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(0, 65)], **{"smooth" : False})
		pointPen.addPoint(*[(65, 200)], **{"smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: smooth=True
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="0" type="move"/>
					<point x="0" y="65"/>
					<point x="65" y="200"/>
					<point x="100" y="200" type="curve" smooth="yes"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 0)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(0, 65)], **{"smooth" : False})
		pointPen.addPoint(*[(65, 200)], **{"smooth" : False})
		pointPen.addPoint(*[(100, 200)], **{"segmentType" : "curve", "smooth" : True})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: no off-curves
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="0" type="move"/>
					<point x="100" y="200" type="curve"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 0)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(100, 200)], **{"segmentType" : "curve", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: 1 off-curve
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="0" type="move"/>
					<point x="50" y="100"/>
					<point x="100" y="200" type="curve"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 0)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(50, 100)], **{"smooth" : False})
		pointPen.addPoint(*[(100, 200)], **{"segmentType" : "curve", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# illegal: 3 off-curves
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="0" type="move"/>
					<point x="0" y="100"/>
					<point x="35" y="125"/>
					<point x="65" y="200"/>
					<point x="100" y="200" type="curve"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 0)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(0, 100)], **{"smooth" : False})
		pointPen.addPoint(*[(35, 125)], **{"smooth" : False})
		pointPen.addPoint(*[(65, 200)], **{"smooth" : False})
		pointPen.addPoint(*[(100, 200)], **{"segmentType" : "curve", "smooth" : False})
		pointPen.endPath()
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testPointQCurve(self):
		# legal
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="0" type="move"/>
					<point x="0" y="65"/>
					<point x="65" y="200"/>
					<point x="100" y="200" type="qcurve"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 0)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(0, 65)], **{"smooth" : False})
		pointPen.addPoint(*[(65, 200)], **{"smooth" : False})
		pointPen.addPoint(*[(100, 200)], **{"segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: start of contour
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="100" y="200" type="qcurve"/>
					<point x="0" y="65"/>
					<point x="65" y="200"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(100, 200)], **{"segmentType" : "qcurve", "smooth" : False})
		pointPen.addPoint(*[(0, 65)], **{"smooth" : False})
		pointPen.addPoint(*[(65, 200)], **{"smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: smooth=True
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="0" type="move"/>
					<point x="0" y="65"/>
					<point x="65" y="200"/>
					<point x="100" y="200" type="qcurve" smooth="yes"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 0)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(0, 65)], **{"smooth" : False})
		pointPen.addPoint(*[(65, 200)], **{"smooth" : False})
		pointPen.addPoint(*[(100, 200)], **{"segmentType" : "qcurve", "smooth" : True})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: no off-curves
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="0" type="move"/>
					<point x="100" y="200" type="qcurve"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 0)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(100, 200)], **{"segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: 1 off-curve
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="0" type="move"/>
					<point x="50" y="100"/>
					<point x="100" y="200" type="qcurve"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 0)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(50, 100)], **{"smooth" : False})
		pointPen.addPoint(*[(100, 200)], **{"segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: 3 off-curves
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="0" type="move"/>
					<point x="0" y="100"/>
					<point x="35" y="125"/>
					<point x="65" y="200"/>
					<point x="100" y="200" type="qcurve"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 0)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(0, 100)], **{"smooth" : False})
		pointPen.addPoint(*[(35, 125)], **{"smooth" : False})
		pointPen.addPoint(*[(65, 200)], **{"smooth" : False})
		pointPen.addPoint(*[(100, 200)], **{"segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)

	def testSpecialCaseQCurve(self):
		# contour with no on curve
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="0"/>
					<point x="0" y="100"/>
					<point x="100" y="100"/>
					<point x="100" y="0"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 0)], **{"smooth" : False})
		pointPen.addPoint(*[(0, 100)], **{"smooth" : False})
		pointPen.addPoint(*[(100, 100)], **{"smooth" : False})
		pointPen.addPoint(*[(100, 0)], **{"smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)

	def testPointTypeOffCurve(self):
		# legal
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="0" type="move"/>
					<point x="0" y="65"/>
					<point x="65" y="200"/>
					<point x="100" y="200" type="curve"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 0)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(0, 65)], **{"smooth" : False})
		pointPen.addPoint(*[(65, 200)], **{"smooth" : False})
		pointPen.addPoint(*[(100, 200)], **{"segmentType" : "curve", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# legal: start of contour
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="65"/>
					<point x="65" y="200"/>
					<point x="100" y="200" type="curve"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 65)], **{"smooth" : False})
		pointPen.addPoint(*[(65, 200)], **{"smooth" : False})
		pointPen.addPoint(*[(100, 200)], **{"segmentType" : "curve", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# before move
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="65"/>
					<point x="0" y="0" type="move"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 65)], **{"smooth" : False})
		pointPen.addPoint(*[(0, 0)], **{"segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# before line
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="65"/>
					<point x="0" y="0" type="line"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 65)], **{"smooth" : False})
		pointPen.addPoint(*[(0, 0)], **{"segmentType" : "line", "smooth" : False})
		pointPen.endPath()
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# smooth=True
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="0" y="65" smooth="yess"/>
					<point x="0" y="0" type="curve"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(0, 65)], **{"smooth" : True})
		pointPen.addPoint(*[(0, 0)], **{"segmentType" : "curve", "smooth" : False})
		pointPen.endPath()
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)

	def testOpenContourLooseOffCurves(self):
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="1" y="2" type="move"/>
					<point x="1" y="2"/>
					<point x="1" y="2"/>
					<point x="1" y="2" type="curve"/>
					<point x="1" y="2"/>
				</contour>
			</outline>
		</glyph>
		"""
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(1, 2)], **{"segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, 2)], **{"smooth" : False})
		pointPen.addPoint(*[(1, 2)], **{"smooth" : False})
		pointPen.addPoint(*[(1, 2)], **{"segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, 2)], **{"smooth" : False})
		pointPen.endPath()
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)

	def testPointIdentifier(self):
		glif = """
		<glyph name="a" format="2">
			<outline>
				<contour>
					<point x="1" y="-2" type="move" identifier="1"/>
					<point x="1" y="-2" type="line" identifier="2"/>
					<point x="1" y="-2" type="curve" identifier="3"/>
					<point x="1" y="-2" type="qcurve" identifier="4"/>
				</contour>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		pointPen.beginPath()
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)

	def testIdentifierConflict(self):
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="guideline1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="point1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "guideline1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		resultGlif = self.pyToGLIF(py)
		resultPy = self.glifToPy(glif)
		self.assertEqual(glif, resultGlif)
		self.assertEqual(py, resultPy)
		# point - point
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="guideline1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="point1"/>
					<point x="1" y="-2" type="line" identifier="point1"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "guideline1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# point - point
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="guideline1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="point1"/>
					<point x="1" y="-2" type="line" identifier="point1"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "guideline1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# point - contour
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="guideline1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="contour1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "guideline1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "contour1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# point - component
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="guideline1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="component1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "guideline1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "component1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# point - guideline
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="guideline1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="guideline1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "guideline1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "guideline1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# point - anchor
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="guideline1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="anchor1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "guideline1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "anchor1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# contour - contour
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="guideline1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="point1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "guideline1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# contour - component
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="guideline1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="point1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="contour1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "guideline1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "contour1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# contour - guideline
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="contour1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="point1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "contour1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# contour - anchor
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="guideline1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="anchor1">
					<point x="1" y="-2" type="move" identifier="point1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "guideline1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "anchor1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# component - component
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="guideline1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="point1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "guideline1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# component - guideline
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="component1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="point1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "component1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# component - anchor
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="guideline1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="point1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="anchor1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "guideline1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "anchor1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# guideline - guideline
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="guideline1"/>
			<guideline x="0" identifier="guideline1"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="point1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "guideline1", "x" : 0}, {"identifier" : "guideline1", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# guideline - anchor
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="anchor1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor2"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="point1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "anchor1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor2", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)
		# anchor - anchor
		glif = """
		<glyph name="a" format="2">
			<guideline x="0" identifier="guideline1"/>
			<guideline x="0" identifier="guideline2"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<anchor x="0" y="0" identifier="anchor1"/>
			<outline>
				<contour identifier="contour1">
					<point x="1" y="-2" type="move" identifier="point1"/>
					<point x="1" y="-2" type="line" identifier="point2"/>
					<point x="1" y="-2" type="curve" identifier="point3"/>
					<point x="1" y="-2" type="qcurve" identifier="point4"/>
				</contour>
				<contour identifier="contour2">
					<point x="1" y="-2" type="move" identifier="point5"/>
				</contour>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component1"/>
				<component base="x" xyScale="1" yxScale="1" xOffset="1" yOffset="1" identifier="component2"/>
			</outline>
		</glyph>
		"""
		py = """
		glyph.name = "a"
		glyph.guidelines = [{"identifier" : "guideline1", "x" : 0}, {"identifier" : "guideline2", "x" : 0}]
		glyph.anchors = [{"identifier" : "anchor1", "x" : 0, "y" : 0}, {"identifier" : "anchor1", "x" : 0, "y" : 0}]
		pointPen.beginPath(**{"identifier" : "contour1"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point1", "segmentType" : "move", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point2", "segmentType" : "line", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point3", "segmentType" : "curve", "smooth" : False})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point4", "segmentType" : "qcurve", "smooth" : False})
		pointPen.endPath()
		pointPen.beginPath(**{"identifier" : "contour2"})
		pointPen.addPoint(*[(1, -2)], **{"identifier" : "point5", "segmentType" : "move", "smooth" : False})
		pointPen.endPath()
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component1"})
		pointPen.addComponent(*["x", (1, 1, 1, 1, 1, 1)], **{"identifier" : "component2"})
		"""
		self.assertRaises(GlifLibError, self.pyToGLIF, py)
		self.assertRaises(GlifLibError, self.glifToPy, glif)


if __name__ == "__main__":
	from ufoLib.test.testSupport import runTests
	runTests()
