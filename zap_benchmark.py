import csv
import json
import random

import requests

# parser = argparse.ArgumentParser(description='ZAP benchmark framework')
#
# parser.add_argument('test_type', type=str,
#                     help='Benchmark migration or benchmark realistic run times')
#
# args = parser.parse_args()

host = 'http://localhost:3000'


def main():
    root_address = post_root()

    wdp_addressess = []
    pdp_addressess = []
    idp_addressess = []

    for wdp_row in read_csv("wdp.csv")[:10]:
        wdp_addressess.append(post_wdp(root_address, int(wdp_row[0]), wdp_row[1]))

    for pdp_row in read_csv("pdp.csv")[:2]:
        pdp_addressess.append(post_wdp(root_address, int(pdp_row[0]), pdp_row[1]))

    for idp_row in read_csv("idp.csv")[:3]:
        idp_addressess.append(post_idp(root_address, int(idp_row[0]), idp_row[1]))

    idos = read_csv('ido.csv')
    for x in range(0, 999):
        ido = idos[x]
        post_ido(root_address, random.choice(idp_addressess), ido[0], ido[1], ido[2], ido[3], ido[4], ido[5], ido[6],
                 ido[7])


def read_csv(csv_file_name):
    csvfile = open(csv_file_name, 'r')
    csv_reader = csv.reader(csvfile, quotechar="'", delimiter=',',
                            quoting=csv.QUOTE_ALL, skipinitialspace=True)

    return [row for row in csv_reader]


def post_ido(root_address, idp_address, id, firstName, lastName, addr, sex, birthYear, birthMonth, birthDay):
    ido_response = requests.post(host + '/api/root/' + root_address
                                 + '/idp/' + idp_address + '/ido/',
                                 data={
                                     'id': id,
                                     'firstName': firstName,
                                     'lastName': lastName,
                                     'addr': addr,
                                     'sex': sex,
                                     'birthYear': birthYear,
                                     'birthMonth': birthMonth,
                                     'birthDay': birthDay,
                                 })
    ido_response_json = json.loads(ido_response.content.decode('utf-8'))
    ido_address = ido_response_json['address']

    return ido_address


def post_wdp(root_address, id, name):
    wdp_response = requests.post(host + "/api/root/" + root_address + "/wdp/",
                                 data={"id": id, "name": name})
    wdp_response_json = json.loads(wdp_response.content.decode('utf-8'))
    wdp_address = wdp_response_json['address']

    return wdp_address


def post_idp(root_address, id, name):
    idp_response = requests.post(host + '/api/root/' + root_address
                                 + '/idp', data={'id': id, 'name': name
                                                 })
    idp_response_json = json.loads(idp_response.content.decode('utf-8'))
    idp_address = idp_response_json['address']

    return idp_address


def post_root():
    root_response = requests.post(host + '/api/root')
    root_response_json = json.loads(root_response.content.decode('utf-8'))
    root_address = root_response_json['address']

    return root_address


if __name__ == '__main__':
    main()
