[
    {'id': '10008', 'piiLeak': True, 'attachments': [
            {'filename': 'Short text more PII.docx', 'PII_leak': True, 'Leaks': [
                    {'entity_group': 'MIDDLENAME', 'score': 0.7505838, 'word': ' john', 'start': 73, 'end': 78
                    },
                    {'entity_group': 'MIDDLENAME', 'score': 0.9017347, 'word': ' doe', 'start': 78, 'end': 82
                    },
                    {'entity_group': 'STREETADDRESS', 'score': 0.9087693, 'word': ' 1234 elm street springfield', 'start': 97, 'end': 125
                    },
                    {'entity_group': 'BUILDINGNUMBER', 'score': 0.60478735, 'word': ' 12345', 'start': 134, 'end': 140
                    },
                    {'entity_group': 'PIN', 'score': 0.54645294, 'word': ' 555', 'start': 179, 'end': 183
                    },
                    {'entity_group': 'PHONE_NUMBER', 'score': 0.30928364, 'word': ' 123 4567', 'start': 183, 'end': 192
                    },
                    {'entity_group': 'SSN', 'score': 0.9886675, 'word': ' 123 45 6789', 'start': 215, 'end': 227
                    },
                    {'entity_group': 'ACCOUNTNUMBER', 'score': 0.89921665, 'word': ' 9876543210', 'start': 247, 'end': 258
                    },
                    {'entity_group': 'STREETADDRESS', 'score': 0.9033114, 'word': ' springfield bank', 'start': 258, 'end': 275
                    },
                    {'entity_group': 'CITY', 'score': 0.99429387, 'word': ' springfield', 'start': 289, 'end': 301
                    },
                    {'entity_group': 'MIDDLENAME', 'score': 0.29805085, 'word': ' 123456', 'start': 379, 'end': 386
                    },
                    {'entity_group': 'MIDDLENAME', 'score': 0.43658632, 'word': ' john', 'start': 386, 'end': 391
                    },
                    {'entity_group': 'FIRSTNAME', 'score': 0.9346378, 'word': ' jane', 'start': 485, 'end': 490
                    },
                    {'entity_group': 'LASTNAME', 'score': 0.58811426, 'word': ' smith', 'start': 490, 'end': 496
                    },
                    {'entity_group': 'CITY', 'score': 0.98500454, 'word': ' springfield', 'start': 505, 'end': 517
                    },
                    {'entity_group': 'CURRENCYCODE', 'score': 0.49261722, 'word': ' dl"', 'start': 616, 'end': 620}]}, {'filename': 'Short Text more PII 2.docx', 'PII_leak': True, 'Leaks': [{'entity_group': 'STREET', 'score': 0.9889782, 'word': ' lakeside manor', 'start': 80, 'end': 95}, {'entity_group': 'DATE', 'score': 0.93250626, 'word': ' april 10th', 'start': 95, 'end': 106}, {'entity_group': 'TIME', 'score': 0.98946625, 'word': ' 6 30 pm', 'start': 106, 'end': 114}, {'entity_group': 'DATE', 'score': 0.97534275, 'word': ' march 25th', 'start': 126, 'end': 137}, {'entity_group': 'SSN', 'score': 0.79463, 'word': ' 555 123 4567', 'start': 137, 'end': 150}, {'entity_group': 'USERNAME', 'score': 0.77717847, 'word': ' venmo', 'start': 172, 'end': 178}, {'entity_group': 'USERNAME', 'score': 0.846381, 'word': ' emilyjones21', 'start': 178, 'end': 191}, {'entity_group': 'FULLNAME', 'score': 0.9822856, 'word': ' emily jones"', 'start': 272, 'end': 285
                    }
                ]
            }
        ], 'agg_score': 2.735469421424187
    },
    {'id': '10007', 'piiLeak': True, 'attachments': [
            {'filename': 'Short text less PII.docx', 'PII_leak': True, 'Leaks': [
                    {'entity_group': 'STREET', 'score': 0.7140117, 'word': ' tapestry woven thread', 'start': 200, 'end': 222
                    }
                ]
            }
        ], 'agg_score': 0.0
    },
    {'id': '10006', 'piiLeak': True, 'attachments': [
            {'filename': 'Long tect seperated PII.docx', 'PII_leak': True, 'Leaks': [
                    {'entity_group': 'CITY', 'score': 0.9887427, 'word': ' springfield', 'start': 26, 'end': 38
                    },
                    {'entity_group': 'STREETADDRESS', 'score': 0.9026599, 'word': ' 1234 elm street', 'start': 239, 'end': 255
                    },
                    {'entity_group': 'BUILDINGNUMBER', 'score': 0.17802218, 'word': ' 555', 'start': 758, 'end': 762
                    },
                    {'entity_group': 'SSN', 'score': 0.8267065, 'word': ' 123 4567', 'start': 762, 'end': 771
                    },
                    {'entity_group': 'STREETADDRESS', 'score': 0.8408009, 'word': ' serf portal', 'start': 771, 'end': 783
                    },
                    {'entity_group': 'STREETADDRESS', 'score': 0.38860267, 'word': ' bridging', 'start': 789, 'end': 798
                    },
                    {'entity_group': 'STREET', 'score': 0.6109514, 'word': ' divide', 'start': 798, 'end': 805
                    },
                    {'entity_group': 'SSN', 'score': 0.9934743, 'word': ' 123 45 6789', 'start': 996, 'end': 1008
                    },
                    {'entity_group': 'STREET', 'score': 0.41110224, 'word': ' indelible mark', 'start': 1250, 'end': 1265
                    },
                    {'entity_group': 'ACCOUNTNUMBER', 'score': 0.9002736, 'word': ' 9876543210', 'start': 1285, 'end': 1296
                    },
                    {'entity_group': 'CITY', 'score': 0.8041867, 'word': ' springfield', 'start': 1425, 'end': 1437
                    },
                    {'entity_group': 'PIN', 'score': 0.4167535, 'word': ' 123456', 'start': 1693, 'end': 1700
                    },
                    {'entity_group': 'CITY', 'score': 0.9954829, 'word': ' hustle bustle', 'start': 1750, 'end': 1764
                    },
                    {'entity_group': 'CITY', 'score': 0.99758345, 'word': ' sanctum springfield', 'start': 2047, 'end': 2067
                    },
                    {'entity_group': 'FIRSTNAME', 'score': 0.85015476, 'word': ' jane', 'start': 2085, 'end': 2090
                    },
                    {'entity_group': 'LASTNAME', 'score': 0.97853297, 'word': ' smith', 'start': 2090, 'end': 2096
                    },
                    {'entity_group': 'CURRENCYCODE', 'score': 0.54316854, 'word': ' dl', 'start': 2392, 'end': 2395
                    }
                ]
            },
            {'filename': 'Long text seperated 2.docx', 'PII_leak': True, 'Leaks': [
                    {'entity_group': 'DATE', 'score': 0.9993802, 'word': ' april 10th', 'start': 260, 'end': 271
                    },
                    {'entity_group': 'TIME', 'score': 0.99917716, 'word': ' 6 30 pm', 'start': 280, 'end': 288
                    },
                    {'entity_group': 'STREET', 'score': 0.9645084, 'word': ' lakeside manor', 'start': 298, 'end': 313
                    },
                    {'entity_group': 'STREET', 'score': 0.8252417, 'word': ' lake undoubtedly', 'start': 343, 'end': 360
                    },
                    {'entity_group': 'DATE', 'score': 0.98776937, 'word': ' march 25th', 'start': 474, 'end': 485
                    },
                    {'entity_group': 'PHONE_NUMBER', 'score': 0.88804555, 'word': ' 555 123 4567', 'start': 539, 'end': 552
                    },
                    {'entity_group': 'CURRENCYNAME', 'score': 0.28375772, 'word': ' venmo', 'start': 756, 'end': 762
                    },
                    {'entity_group': 'USERNAME', 'score': 0.96115476, 'word': ' emilyjones21', 'start': 762, 'end': 775
                    },
                    {'entity_group': 'STREET', 'score': 0.833081, 'word': ' lakeside manor', 'start': 1198, 'end': 1213
                    },
                    {'entity_group': 'FIRSTNAME', 'score': 0.85294825, 'word': ' emily', 'start': 1257, 'end': 1263
                    },
                    {'entity_group': 'MIDDLENAME', 'score': 0.94090694, 'word': ' jones"', 'start': 1263, 'end': 1270}]}], 'agg_score': 3.0672244186010578}, {'id': '10005', 'piiLeak': True, 'title': [{'entity_group': 'FIRSTNAME', 'score': 0.8032697, 'word': ' Short', 'start': 0, 'end': 5}, {'entity_group': 'LASTNAME', 'score': 0.8847924, 'word': ' Bursts', 'start': 5, 'end': 12}], 'attachments': [{'filename': 'Short bursts.docx', 'PII_leak': True, 'Leaks': [{'entity_group': 'JOBDESCRIPTOR', 'score': 0.84299713, 'word': ' great', 'start': 119, 'end': 125}, {'entity_group': 'JOBTYPE', 'score': 0.44054556, 'word': ' explorer', 'start': 125, 'end': 134}, {'entity_group': 'JOBTITLE', 'score': 0.36626962, 'word': ' truth master builder', 'start': 134, 'end': 155}, {'entity_group': 'MIDDLENAME', 'score': 0.5235174, 'word': ' john', 'start': 1144, 'end': 1149}, {'entity_group': 'MIDDLENAME', 'score': 0.6413196, 'word': ' doe', 'start': 1149, 'end': 1153}, {'entity_group': 'STREETADDRESS', 'score': 0.85458565, 'word': ' 1234 elm street springfield', 'start': 1168, 'end': 1196}, {'entity_group': 'BUILDINGNUMBER', 'score': 0.5179985, 'word': ' 12345', 'start': 1205, 'end': 1211}, {'entity_group': 'PIN', 'score': 0.35206777, 'word': ' 555', 'start': 1250, 'end': 1254}, {'entity_group': 'PHONE_NUMBER', 'score': 0.50476205, 'word': ' 123 4567', 'start': 1254, 'end': 1263}, {'entity_group': 'SSN', 'score': 0.99249434, 'word': ' 123 45 6789', 'start': 1286, 'end': 1298}, {'entity_group': 'ACCOUNTNUMBER', 'score': 0.986652, 'word': ' 9876543210', 'start': 1318, 'end': 1329}, {'entity_group': 'CITY', 'score': 0.96064186, 'word': ' springfield', 'start': 1360, 'end': 1372}, {'entity_group': 'FIRSTNAME', 'score': 0.3469322, 'word': ' 123456', 'start': 1450, 'end': 1457}, {'entity_group': 'MIDDLENAME', 'score': 0.5786184, 'word': ' jane', 'start': 1556, 'end': 1561}, {'entity_group': 'LASTNAME', 'score': 0.9703259, 'word': ' smith', 'start': 1561, 'end': 1567}, {'entity_group': 'CITY', 'score': 0.96945894, 'word': ' springfield', 'start': 1576, 'end': 1588}, {'entity_group': 'JOBDESCRIPTOR', 'score': 0.8182508, 'word': ' great', 'start': 1942, 'end': 1948}, {'entity_group': 'JOBTYPE', 'score': 0.47556177, 'word': ' explorer', 'start': 1948, 'end': 1957}, {'entity_group': 'JOBTITLE', 'score': 0.33484125, 'word': ' truth master builder', 'start': 1957, 'end': 1978}, {'entity_group': 'MIDDLENAME', 'score': 0.58604324, 'word': ' john', 'start': 3138, 'end': 3143}, {'entity_group': 'MIDDLENAME', 'score': 0.611448, 'word': ' doe', 'start': 3143, 'end': 3147}, {'entity_group': 'STREETADDRESS', 'score': 0.82480896, 'word': ' 1234 elm street springfield', 'start': 3162, 'end': 3190}, {'entity_group': 'BUILDINGNUMBER', 'score': 0.5942816, 'word': ' 12345', 'start': 3199, 'end': 3205}]}, {'filename': 'Short bursts 2.docx', 'PII_leak': True, 'Leaks': [{'entity_group': 'STREET', 'score': 0.9929036, 'word': ' blue lagoon', 'start': 142, 'end': 154}, {'entity_group': 'DATE', 'score': 0.9451196, 'word': ' march 15th', 'start': 154, 'end': 165}, {'entity_group': 'TIME', 'score': 0.9965339, 'word': ' 7 00 pm', 'start': 165, 'end': 173}, {'entity_group': 'FIRSTNAME', 'score': 0.5372787, 'word': ' sarah', 'start': 173, 'end': 179}, {'entity_group': 'FIRSTNAME', 'score': 0.9804002, 'word': ' camaraderie', 'start': 566, 'end': 578}, {'entity_group': 'DATE', 'score': 0.81585246, 'word': ' march 1st', 'start': 847, 'end': 857}, {'entity_group': 'STREET', 'score': 0.2590172, 'word': ' john', 'start': 967, 'end': 972}, {'entity_group': 'LASTNAME', 'score': 0.6027929, 'word': ' smith', 'start': 972, 'end': 978}, {'entity_group': 'TIME', 'score': 0.9761126, 'word': ' 6 45 pm', 'start': 1030, 'end': 1038}, {'entity_group': 'FIRSTNAME', 'score': 0.864807, 'word': ' sarah', 'start': 1080, 'end': 1086}, {'entity_group': 'FIRSTNAME', 'score': 0.70774984, 'word': ' camaraderie', 'start': 1145, 'end': 1157}]}], 'agg_score': 4.013903764895789}, {'id': '10003', 'piiLeak': False, 'agg_score': 0}, {'id': '10001', 'piiLeak': True, 'title': [{'entity_group': 'FIRSTNAME', 'score': 0.5479093, 'word': ' John', 'start': 0, 'end': 4}, {'entity_group': 'STREETADDRESS', 'score': 0.98973805, 'word': ' 1234 Elm Street,', 'start': 28, 'end': 45}, {'entity_group': 'CITY', 'score': 0.8217468, 'word': ' Springfield,', 'start': 45, 'end': 58}, {'entity_group': 'ZIPCODE', 'score': 0.9743819, 'word': ' 12345.', 'start': 67, 'end': 74}, {'entity_group': 'EMAIL', 'score': 0.9994993, 'word': ' johndoe@email.com', 'start': 95, 'end': 113}, {'entity_group': 'PHONE_NUMBER', 'score': 0.9911221, 'word': ' 555-123-4567.', 'start': 136, 'end': 150}, {'entity_group': 'SSN', 'score': 0.9868826, 'word': ' 123-45-678', 'start': 180, 'end': 191}, {'entity_group': 'COMPANY_NAME', 'score': 0.9394711, 'word': ' Acme', 'start': 207, 'end': 212}, {'entity_group': 'PIN', 'score': 0.87060857, 'word': ' 123456.', 'start': 240, 'end': 248}], 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              'agg_score': 2.4022222222222225}]