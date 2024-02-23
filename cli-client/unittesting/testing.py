import unittest
from argparse import Namespace
from se2305 import searchtitle,title,searchname,name,bygenre,newtitles,newnames,newcrew,newakas,newepisode,newratings,newprincipals,healthcheck,resetall,top10genre

class TestYourCLI(unittest.TestCase):
    def test_aanewtitles_valid_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv')
        result = newtitles(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "titlebasics data added"',result.text) 

    def test_abnewtitles_edge_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\titles.tsv')
        result = newtitles(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "titlebasics data added"',result.text)

    def test_newtitles_invalid_null(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\null.tsv')
        result = newtitles(args)
        self.assertEqual(result.status_code,500)
        self.assertIn(' "error": "Internal server error"',result.text) 

    def test_acnewtitles_invalid_input1(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\name.tsv')
        result = newtitles(args)
        self.assertEqual(result.status_code,400)
        self.assertIn('"Unknown column',result.text)

    def test_adnewtitles_invalid_input2(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv')
        result = newtitles(args)
        self.assertEqual(result.status_code,500)
        self.assertIn('"Internal server error',result.text)

    def test_aesearchtitle_valid_input(self):
        args = Namespace(scope='searchtitle', titlepart='Kleb')
        result = searchtitle(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"titleID": "tt0000929"',result.text)

    def test_afsearchtitle_invalid_input(self):
        args = Namespace(scope='searchtitle', titlepart='Νύχτα')
        result = searchtitle(args)
        self.assertEqual(result.status_code,404)
        self.assertEqual(result.text,'[]\n')

    def test_agtitle_valid_input(self):
        args = Namespace(scope='title', titleID='tt0000929')
        result = title(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"originalTitle": "Klebolin klebt alles"',result.text)

    def test_ahtitle_invalid_input(self):
        args = Namespace(scope='title', titleID='tt4444444')
        result = title(args)
        self.assertEqual(result.status_code,404)
        self.assertEqual(result.text,'{\n    "message": "Title not found"\n}\n')

    def test_aisearchname_valid_input(self):
        args = Namespace(scope='searchname', name='Ernst')
        result = searchname(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"titleID": "tt0000929"',result.text)

    def test_ajsearchname_invalid_input(self):
        args = Namespace(scope='searchname', name='Pavlos')
        result = searchname(args)
        self.assertEqual(result.status_code,404)
        self.assertEqual(result.text,'[]\n')

    def test_akname_valid_input(self):
        args = Namespace(scope='name', nameid='nm0066941')
        result = name(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"name": "Ernst Behmer"',result.text)

    def test_alname_invalid_input(self):
        args = Namespace(scope='name', nameid='nm4444444')
        result = name(args)
        self.assertEqual(result.status_code,404)
        self.assertIn('"Contributor not found"',result.text)

    def test_ambygenre_valid_input(self):
        args = Namespace(scope='bygenre', genre='Comedy',min='5',yrFrom='1998',yrTo='2030')
        result = bygenre(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"titleID": "tt0095469"',result.text)

    def test_anbygenre_invalid_input(self):
        args = Namespace(scope='bygenre', genre='Comedy',min='5',yrFrom='2040',yrTo='2050')
        result = bygenre(args)
        self.assertEqual(404,result.status_code)
        self.assertEqual(result.text,'[]\n')

    def test_aonewnames_valid_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\name.tsv')
        result = newnames(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "namebasics data added"',result.text)

    def test_apnewnames_edge_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\names.tsv')
        result = newnames(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "namebasics data added"',result.text)
    
    def test_newnames_invalid_null(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\null.tsv')
        result = newnames(args)
        self.assertEqual(result.status_code,500)
        self.assertIn(' "error": "Internal server error"',result.text) 

    def test_aqnewnames_invalid_input1(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv')
        result = newnames(args)
        self.assertEqual(result.status_code,400)
        self.assertIn('"Unknown column',result.text)

    def test_arnewnames_invalid_input2(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\name.tsv')
        result = newnames(args)
        self.assertEqual(result.status_code,500)
        self.assertIn('"Internal server error',result.text)

    def test_asnewcrew_valid_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\crew.tsv')
        result = newcrew(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "crew data added"',result.text)

    def test_atnewcrew_edge_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\crews.tsv')
        result = newcrew(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "crew data added"',result.text)

    def test_newcrew_invalid_null(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\null.tsv')
        result = newcrew(args)
        self.assertEqual(result.status_code,500)
        self.assertIn(' "error": "Internal server error"',result.text) 

    def test_aunewcrew_invalid_input1(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv')
        result = newcrew(args)
        self.assertEqual(result.status_code,400)
        self.assertIn('"Unknown column',result.text)

    def test_avnewcrew_invalid_input2(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\crew.tsv')
        result = newcrew(args)
        self.assertEqual(result.status_code,500)
        self.assertIn('"Internal server error',result.text)

    def test_awnewakas_valid_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\aka.tsv')
        result = newakas(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "akas data added"',result.text)

    def test_axnewakas_edge_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\akas.tsv')
        result = newakas(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "akas data added"',result.text)

    def test_newakas_invalid_null(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\null.tsv')
        result = newakas(args)
        self.assertEqual(result.status_code,500)
        self.assertIn(' "error": "Internal server error"',result.text) 

    def test_aynewakas_invalid_input1(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv')
        result = newakas(args)
        self.assertEqual(result.status_code,400)
        self.assertIn('"Unknown column',result.text)

    def test_aznewakas_invalid_input2(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\aka.tsv')
        result = newakas(args)
        self.assertEqual(result.status_code,500)
        self.assertIn('"Internal server error',result.text)
        
    def test_banewepisode_valid_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\episode.tsv')
        result = newepisode(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "episode data added"',result.text)  

    def test_bbnewepisode_edge_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\episodes.tsv')
        result = newepisode(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "episode data added"',result.text)

    def test_newepisode_invalid_null(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\null.tsv')
        result = newepisode(args)
        self.assertEqual(result.status_code,500)
        self.assertIn(' "error": "Internal server error"',result.text) 

    def test_bcnewepisode_invalid_input1(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv')
        result = newepisode(args)
        self.assertEqual(result.status_code,400)
        self.assertIn('"Unknown column',result.text)

    def test_bdnewepisode_invalid_input2(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\episode.tsv')
        result = newepisode(args)
        self.assertEqual(result.status_code,500)
        self.assertIn('"Internal server error',result.text)

    def test_benewratings_valid_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\rating.tsv')
        result = newratings(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "ratings data added"',result.text)  

    def test_bfnewratings_edge_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\ratings.tsv')
        result = newratings(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "ratings data added"',result.text)
    
    def test_newratings_invalid_null(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\null.tsv')
        result = newratings(args)
        self.assertEqual(result.status_code,500)
        self.assertIn(' "error": "Internal server error"',result.text) 

    def test_bgnewratings_invalid_input1(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv')
        result = newratings(args)
        self.assertEqual(result.status_code,400)
        self.assertIn('"Unknown column',result.text)

    def test_bhnewratings_invalid_input2(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\rating.tsv')
        result = newratings(args)
        self.assertEqual(result.status_code,500)
        self.assertIn('"Internal server error',result.text)

    def test_binewprincipals_valid_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\principal.tsv')
        result = newprincipals(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "principals data added"',result.text)  

    def test_bjnewprincipals_edge_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\principals.tsv')
        result = newprincipals(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "principals data added"',result.text)

    def test_newprincipals_invalid_null(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\null.tsv')
        result = newprincipals(args)
        self.assertEqual(result.status_code,500)
        self.assertIn(' "error": "Internal server error"',result.text) 

    def test_bknewprincipals_invalid_input1(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv')
        result = newprincipals(args)
        self.assertEqual(result.status_code,400)
        self.assertIn('"Unknown column',result.text)

    def test_blnewprincipals_invalid_input2(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\principal.tsv')
        result = newprincipals(args)
        self.assertEqual(result.status_code,500)
        self.assertIn('"Internal server error',result.text)
    
    def test_bmhealthcheck(self):
        result = healthcheck()
        self.assertEqual(result.status_code,200)
        self.assertIn('"database": "Connected"',result.text)
    
    def test_bntop10genre(self):
        result = top10genre()
        self.assertEqual(result.status_code,200)

    def test_boresetall(self):
        result = resetall()
        self.assertEqual(result.status_code,200)
        self.assertIn('"Database repopulated successfully"',result.text)
    
    
     
if __name__ == '__main__':
    unittest.main()