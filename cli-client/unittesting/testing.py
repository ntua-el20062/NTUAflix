import unittest
from argparse import Namespace
from se2305 import searchtitle,title,searchname,name,bygenre,newtitles,newnames,newcrew,newakas,newepisode,newratings,newprincipals,healthcheck,resetall,top10genre

class TestYourCLI(unittest.TestCase):
    def test_aanewtitles_valid_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv',format='json')
        result = newtitles(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "titlebasics data added"',result.text) 

    def test_abnewtitles_edge_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\titles.tsv',format='json')
        result = newtitles(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "titlebasics data added"',result.text)

    def test_newtitles_invalid_null(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\null_title.tsv',format='json')
        result = newtitles(args)
        self.assertEqual(result.status_code,204)
        self.assertIn('',result.text) 

    def test_acnewtitles_invalid_input1(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\name.tsv',format='json')
        result = newtitles(args)
        self.assertEqual(result.status_code,400)
        self.assertIn('"Unknown column',result.text)

    def test_adnewtitles_invalid_input2(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv',format='json')
        result = newtitles(args)
        self.assertEqual(result.status_code,500)
        self.assertIn('"Internal server error',result.text)

    def test_aesearchtitle_valid_input(self):
        args = Namespace(scope='searchtitle', titlepart='Kleb',format='json')
        result = searchtitle(args)  
        self.assertEqual(result.status_code, 200)
        self.assertIn('tt0000929', result.text)  

    def test_afsearchtitle_invalid_input(self):
        args = Namespace(scope='searchtitle', titlepart='Νύχτα',format='json')
        result = searchtitle(args)
        self.assertEqual(result.status_code,404)
        self.assertEqual(result.text,'[]\n')

    def test_agtitle_valid_input(self):
        args = Namespace(scope='title', titleID='tt0000929',format='json')
        result = title(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"originalTitle": "Klebolin klebt alles"',result.text)

    def test_ahtitle_invalid_input(self):
        args = Namespace(scope='title', titleID='tt4444444',format='json')
        result = title(args)
        self.assertEqual(result.status_code,404)
        self.assertEqual(result.text,'{\n    "message": "Title not found"\n}\n')

    def test_aisearchname_valid_input(self):
        args = Namespace(scope='searchname', name='Ernst',format='json')
        result = searchname(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"titleID": "tt0000929"',result.text)

    def test_ajsearchname_invalid_input(self):
        args = Namespace(scope='searchname', name='Pavlos',format='json')
        result = searchname(args)
        self.assertEqual(result.status_code,404)
        self.assertEqual(result.text,'[]\n')

    def test_akname_valid_input(self):
        args = Namespace(scope='name', nameid='nm0066941',format='json')
        result = name(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"name": "Ernst Behmer"',result.text)

    def test_alname_invalid_input(self):
        args = Namespace(scope='name', nameid='nm4444444',format='json')
        result = name(args)
        self.assertEqual(result.status_code,404)
        self.assertIn('"Contributor not found"',result.text)

    def test_ambygenre_valid_input(self):
        args = Namespace(scope='bygenre', genre='Comedy',min='5',yrFrom='1998',yrTo='2030',format='json')
        result = bygenre(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"titleID": "tt0095469"',result.text)

    def test_anbygenre_invalid_input(self):
        args = Namespace(scope='bygenre', genre='Comedy',min='5',yrFrom='2040',yrTo='2050',format='json')
        result = bygenre(args)
        self.assertEqual(404,result.status_code)
        self.assertEqual(result.text,'[]\n')

    def test_aonewnames_valid_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\name.tsv',format='json')
        result = newnames(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "namebasics data added"',result.text)

    def test_apnewnames_edge_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\names.tsv',format='json')
        result = newnames(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "namebasics data added"',result.text)
    
    def test_newnames_invalid_null(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\null_name.tsv',format='json')
        result = newnames(args)
        self.assertEqual(result.status_code,204)
        self.assertIn('',result.text) 

    def test_aqnewnames_invalid_input1(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv',format='json')
        result = newnames(args)
        self.assertEqual(result.status_code,400)
        self.assertIn('"Unknown column',result.text)

    def test_arnewnames_invalid_input2(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\name.tsv',format='json')
        result = newnames(args)
        self.assertEqual(result.status_code,500)
        self.assertIn('"Internal server error',result.text)

    def test_asnewcrew_valid_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\crew.tsv',format='json')
        result = newcrew(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "crew data added"',result.text)

    def test_atnewcrew_edge_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\crews.tsv',format='json')
        result = newcrew(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "crew data added"',result.text)

    def test_newcrew_invalid_null(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\null_crew.tsv',format='json')
        result = newcrew(args)
        self.assertEqual(result.status_code,204)
        self.assertIn('',result.text) 

    def test_aunewcrew_invalid_input1(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv',format='json')
        result = newcrew(args)
        self.assertEqual(result.status_code,400)
        self.assertIn('"Unknown column',result.text)

    def test_avnewcrew_invalid_input2(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\crew.tsv',format='json')
        result = newcrew(args)
        self.assertEqual(result.status_code,500)
        self.assertIn('"Internal server error',result.text)

    def test_awnewakas_valid_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\aka.tsv',format='json')
        result = newakas(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "akas data added"',result.text)

    def test_axnewakas_edge_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\akas.tsv',format='json')
        result = newakas(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "akas data added"',result.text)

    def test_newakas_invalid_null(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\null_aka.tsv',format='json')
        result = newakas(args)
        self.assertEqual(result.status_code,204)
        self.assertIn('',result.text) 

    def test_aynewakas_invalid_input1(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv',format='json')
        result = newakas(args)
        self.assertEqual(result.status_code,400)
        self.assertIn('"Unknown column',result.text)

    def test_aznewakas_invalid_input2(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\aka.tsv',format='json')
        result = newakas(args)
        self.assertEqual(result.status_code,500)
        self.assertIn('"Internal server error',result.text)
        
    def test_banewepisode_valid_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\episode.tsv',format='json')
        result = newepisode(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "episode data added"',result.text)  

    def test_bbnewepisode_edge_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\episodes.tsv',format='json')
        result = newepisode(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "episode data added"',result.text)

    def test_newepisode_invalid_null(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\null_episode.tsv',format='json')
        result = newepisode(args)
        self.assertEqual(result.status_code,204)
        self.assertIn('',result.text) 

    def test_bcnewepisode_invalid_input1(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv',format='json')
        result = newepisode(args)
        self.assertEqual(result.status_code,400)
        self.assertIn('"Unknown column',result.text)

    def test_bdnewepisode_invalid_input2(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\episode.tsv',format='json')
        result = newepisode(args)
        self.assertEqual(result.status_code,500)
        self.assertIn('"Internal server error',result.text)

    def test_benewratings_valid_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\rating.tsv',format='json')
        result = newratings(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "ratings data added"',result.text)  

    def test_bfnewratings_edge_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\ratings.tsv',format='json')
        result = newratings(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "ratings data added"',result.text)
    
    def test_newratings_invalid_null(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\null_rating.tsv',format='json')
        result = newratings(args)
        self.assertEqual(result.status_code,204)
        self.assertIn('',result.text) 

    def test_bgnewratings_invalid_input1(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv',format='json')
        result = newratings(args)
        self.assertEqual(result.status_code,400)
        self.assertIn('"Unknown column',result.text)

    def test_bhnewratings_invalid_input2(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\rating.tsv',format='json')
        result = newratings(args)
        self.assertEqual(result.status_code,500)
        self.assertIn('"Internal server error',result.text)

    def test_binewprincipals_valid_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\principal.tsv',format='json')
        result = newprincipals(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "principals data added"',result.text)  

    def test_bjnewprincipals_edge_input(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\principals.tsv',format='json')
        result = newprincipals(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"status": "principals data added"',result.text)

    def test_newprincipals_invalid_null(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\null_principal.tsv',format='json')
        result = newprincipals(args)
        self.assertEqual(result.status_code,204)
        self.assertIn('',result.text) 

    def test_bknewprincipals_invalid_input1(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\title.tsv',format='json')
        result = newprincipals(args)
        self.assertEqual(result.status_code,400)
        self.assertIn('"Unknown column',result.text)

    def test_blnewprincipals_invalid_input2(self):
        args = Namespace(scope='filename', filename='C:\\Users\\pavlo\\principal.tsv',format='json')
        result = newprincipals(args)
        self.assertEqual(result.status_code,500)
        self.assertIn('"Internal server error',result.text)
    
    def test_bmhealthcheck(self):
        args = Namespace(format='json')
        result = healthcheck(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"database": "Connected"',result.text)
    
    def test_bntop10genre(self):
        args = Namespace(format='json')
        result = top10genre(args)
        self.assertEqual(result.status_code,200)

    def test_boresetall(self):
        args = Namespace(format='json')
        result = resetall(args)
        self.assertEqual(result.status_code,200)
        self.assertIn('"Database repopulated successfully"',result.text)
    
    
     
if __name__ == '__main__':
    unittest.main()