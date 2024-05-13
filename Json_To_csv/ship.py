import json
import csv
import re
import sqlite3

'''
This Module is Json to csv converter for shipping requests. It also stores data in database.
Extract: A complex Json collection: This collections contains multiple JSON requests. Each requests has multiple objects, arrays and key-value pairs
Transform: There is a business logic keyed in 
Load: CSV file for selected data
'''


connection = sqlite3.connect('shipment1.sqllite')
cursor = connection.cursor()
cursor.executescript('''
DROP TABLE IF EXISTS SHIPMENT;

CREATE TABLE  IF NOT EXISTS SHIPMENT(
    Surrogate_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Number INTEGER NOT NULL,
    Key TEXT UNIQUE,
    Request_type TEXT,
    Region TEXT,
    Name TEXT,
    Origin_cntry_cd TEXT,
    Destination_cntry_cd TEXT,
    service_typ TEXT,
    packaging_type TEXT,
    Label_type TEXT,
    paymentType_shippingChargesPayment TEXT,
    paymentType_dutiesPayment_customsClearanceDetail TEXT,
    shipment_specialServiceType TEXT,
    package_specialServiceType TEXT
)

''')


DELIMITER = '|'
# INPUT_FILE_NAME = 'input_file.json' # this file contains sub-folder 'Non US Domestic' inside International folder
# INPUT_FILE_NAME = '../Updated.json'
# INPUT_FILE_NAME = '/Users/kalpandalal/IdeaProjects/p4ye/Searching_tool/8.json'
# INPUT_FILE_NAME = '/Users/kalpandalal/IdeaProjects/p4ye/Searching_tool/Ship_collection_DT0325.json'
INPUT_FILE_NAME = '/Users/kalpandalal/IdeaProjects/p4ye/Searching_tool/Ship_collection_DT0401.json'

# OUTPUT_FILE_NAME = 'output/search_tool.csv'
# OUTPUT_FILE_NAME = '../output/op4.csv'
OUTPUT_FILE_NAME = '../output/op5.csv'
COUNTER = 1
LIMITED_MODE = 0  # 0 is off and 1 is on
searched_text = 'ACCESSIBLE'  # input("What are you looking for: ")

typeOfReq_cnt = 0
new_request_cnt = 0
paymentTypeDutiesPaymentCustomsClearanceDetail = ''
region_based_count = 0
newline_position = -1
region = ""
# Below list contains Insomnia/Postman name of all API requests
request_name = []
# Below list is a list of dictionarie
OUTPUT_LIST = []
SORTED_LST = []
create_shipment_tally = dict()
other_req_tally = dict()

Origin_cntry_cd = ""
Destination_cntry_cd = ""
service_typ = ""
shipment_service_type = list()
package_service_type = list()

matched_list = list()

Number = 0
Name = ""
Json_Request = ""
dangerousGoods_accessibility = ""

headers = ['Number', 'Key', 'request_type', 'Region', 'Name', 'Origin_cntry_cd', 'Destination_cntry_cd', 'service_typ',
           'packaging_type',
           # 'pickup_type',
           'Label_info',
           # 'image_type',
           # 'labelStock_type',
           # 'labelResponseOptions',
           # 'shipAction', 'processingOptionType',
           'paymentType_shippingChargesPayment',
           'paymentType_dutiesPayment_customsClearanceDetail',
           # 'oneLabelAtATime',
           # 'dangerousGoods_accessibility',
           'shipment_specialServiceType', 'package_specialServiceType'
           # , 'Json_Request'
           ]

create_shipment_counter = 0
create_shipment_US_Domestic_counter = 0
create_shipment_Non_US_Domestic_counter = 1999
create_shipment_International_counter = 2999
create_shipment_Intra_Europe_counter = 4499
create_shipment_Intra_CA_counter = 4799

Cancel_Shipment_counter = 4999
Validate_Shipment_counter = 5999
Retrieve_Async_Ship_counter = 6999
Create_Tag_counter = 7999
Cancel_Tag_counter = 8999


def generate_key(request_type: str, region: str) -> str:
    """
    Based on teh request type, create a range

    `Type of request`	`Range`
    Create Shipment	    SH0001-SH4999
    Cancel Shipment 	SH5000-SH5999
    Validate Shipment	SH6000-SH6999
    Retrieve Shipment	SH7000-SH7999
    Create Tag	        SH8000-SH8999
    Cancel Tag	        SH9000-SH9999

    :param request_type: type of request
    :param region: region
    :return:
    """
    global Cancel_Shipment_counter, Validate_Shipment_counter, Retrieve_Async_Ship_counter, Create_Tag_counter, \
        Cancel_Tag_counter, create_shipment_counter, create_shipment_US_Domestic_counter, \
        create_shipment_Non_US_Domestic_counter, create_shipment_International_counter, \
        create_shipment_Intra_Europe_counter, create_shipment_Intra_CA_counter
    match request_type:
        case "Create Shipment":
            if region == 'US Domestic':
                create_shipment_US_Domestic_counter += 1
                return f"SH{create_shipment_US_Domestic_counter:04d}"
            elif region == 'Non US Domestic':
                create_shipment_Non_US_Domestic_counter += 1
                return f"SH{create_shipment_Non_US_Domestic_counter}"
            elif region == 'International':
                create_shipment_International_counter += 1
                return f"SH{create_shipment_International_counter}"
            elif region == 'Intra Europe':
                create_shipment_Intra_Europe_counter += 1
                return f"SH{create_shipment_Intra_Europe_counter}"
            elif region == 'Intra CA':
                create_shipment_Intra_CA_counter += 1
                return f"SH{create_shipment_Intra_CA_counter}"
            else:
                print("Request type:", request_type)
                print("region:", region)
                raise ValueError("Cannot find valid Request Type")
            # create_shipment_counter += 1
            # return f"SH{create_shipment_counter:04d}"
        case "Cancel Shipment":
            Cancel_Shipment_counter += 1
            return f"SH{Cancel_Shipment_counter}"
        case "Validate Shipment":
            Validate_Shipment_counter += 1
            return f"SH{Validate_Shipment_counter}"
        case "Retrieve Async Ship":
            Retrieve_Async_Ship_counter += 1
            return f"SH{Retrieve_Async_Ship_counter}"
        case "Create Tag":
            Create_Tag_counter += 1
            return f"SH{Create_Tag_counter}"
        case "Cancel Tag":
            Cancel_Tag_counter += 1
            return f"SH{Cancel_Tag_counter}"
        case _:
            print("Request type", request_type)
            raise ValueError("Cannot find valid Request Type")


# Function to clean and extract special service types
def clean_special_service(special_service_obj: list) -> list:
    """
    This will take various special service types and returns a list so that we can populate it in a column.
    :param special_service_obj:
    :return: list of various special service types
    """
    if not special_service_obj:
        return list()
    return [val if len(val) > 0 else "" for val in special_service_obj]


def append_DG(package_service_type: list, specialServiceType: str) -> list:
    """
    This will append accessible or inacessible to DANGEROUS_GOODS--like 'DANGEROUS_GOODS(INACCESSIBLE)'

    :param package_service_type:
    :param specialServiceType:
    :return:
    """
    updated_packageServiceType = list()
    for packageServiceType in package_service_type:
        if packageServiceType == 'DANGEROUS_GOODS':
            packageServiceType += f"({specialServiceType})"
        updated_packageServiceType.append(packageServiceType)
    return updated_packageServiceType


def append_SignOption(package_service_type: list, specialServiceType: str) -> list:
    """
    This will append signature option detail to special service signature option--like SIGNATURE_OPTION(ADULT)
    :param package_service_type:
    :param specialServiceType:
    :return:
    """
    updated_packageServiceType = list()
    for packageServiceType in package_service_type:
        if packageServiceType == 'SIGNATURE_OPTION':
            packageServiceType += f"({specialServiceType})"
        updated_packageServiceType.append(packageServiceType)
    return updated_packageServiceType


def replace_multiple_underscroes_regex_remove_last_underscore_slice(text: str) -> str:
    """
    This function will address three issues.
    1. replace multiple underscores "__" or "___" with single underscore "_"
    2. remove leading or trailing spaces
    3. some name ends with underscore "_"; remove this last character, underscore "_"
    :param text: modified text wherein special characters are replaced with underscore "_"
    :return: final text
    """

    #  replace multiple underscores "__" or "___" with single underscore "_"
    interim_text = re.sub(r'_+', '_', text)

    # remove leading or trailing spaces
    interim_text = interim_text.strip()

    # some name ends with underscore "_"; remove this last character, underscore "_"
    final_text = interim_text[:-1] if interim_text.endswith("_") else interim_text

    return final_text


def replace_special_characters_with_underscore(req_name: str) -> str:
    """
    Replaces all special characters in a string with '_' in order to beautify name parameters
    :param req_name: Sending name of individual request
    :return:  A new string with specific special characters replaced by '_'.
    """
    # definition of trans table with specified characters
    transalation_table = str.maketrans("""!@#$%^&*()_-+={}[]|\\:;\"'<,>.?~/` """, "".join(["_" for _ in range(33)]))
    modified_request = req_name.translate(transalation_table)

    final_text = replace_multiple_underscroes_regex_remove_last_underscore_slice(modified_request)

    return final_text


def create_output_from_json(raw_json: str, individual_request_name: str, request_type: str, region: str = '') -> None:
    """
    1. parses JSON file
    2. Extract relevant data
    3. Transform them in proper format
    4. load them in list of dictionary
    :param raw_json:
    :param individual_request_name:
    :param request_type:
    :param region:
    :return: None
    """
    global COUNTER, OUTPUT_LIST, new_request_cnt
    inner_json = None
    try:
        inner_json = json.loads(raw_json)
    except ValueError as ve:
        print(" $$$$$$$$$$$$$  ABEND $$$$$$$$$$$$$")
        print("Value Error: ", ve)
        print(individual_request_name)

    except Exception as exception:
        print(" $$$$$$$$$$$$$  ABEND $$$$$$$$$$$$$")
        print("An unexpected error: ", exception)
        print(individual_request_name)

    has_key_already_assigned = False
    if (individual_request_name.startswith('SH') and individual_request_name[2:6].isdigit() and
            individual_request_name[6:7] == '_'):
                has_key_already_assigned = True

    Key = generate_key(type_of_request, region)
    Number = int(Key[2:])
    Name = replace_special_characters_with_underscore(individual_request_name)
    if not has_key_already_assigned:
        new_request_cnt = new_request_cnt + 1
        Name = Key + "_" + Name
        print(f"{new_request_cnt}. {Name}")
    # below is for debugging if there are any other issues
    else:
        if (individual_request_name[7:9] == 'SH' and individual_request_name[9:13].isdigit()
                and individual_request_name[13:14] == '_'):
            print("Problem request $$$$$$: ",individual_request_name)

    Origin_cntry_cd = inner_json["requestedShipment"]["shipper"]["address"].get("countryCode", "")
    Destination_cntry_cd = inner_json["requestedShipment"]["recipients"][0]["address"].get("countryCode", "")
    service_typ = inner_json["requestedShipment"].get('serviceType', {})

    shipment_service_type = list()
    shipment_SpecialService = inner_json.get("requestedShipment", {}).get("shipmentSpecialServices", {})
    if shipment_SpecialService:
        tmp_special_service = clean_special_service(shipment_SpecialService.get("specialServiceTypes", {}))
        if tmp_special_service:
            shipment_service_type.extend(tmp_special_service)
        else:
            shipment_service_type = list()
    else:
        shipment_service_type = list()

    if shipment_service_type:
        shipment_service_type = list(set(shipment_service_type))
        temp_shipment_specialServiceType = ", ".join(shipment_service_type)
    else:
        temp_shipment_specialServiceType = ""

    packaging_type = inner_json["requestedShipment"].get('packagingType',  "")
    # pickup_type = inner_json["requestedShipment"].get('pickupType',  "")
    labelSpecification_obj = inner_json["requestedShipment"].get('labelSpecification', {})
    if labelSpecification_obj:
        image_type = labelSpecification_obj.get('imageType', "")
        labelStock_type = labelSpecification_obj.get('labelStockType', "")
    else:
        image_type = ''
        labelStock_type = ''

    package_service_type = list()
    dangerousGoods_accessibility = ""
    signatureOptionType = ""
    package_SpecialService_obj = inner_json.get("requestedShipment", {}).get("requestedPackageLineItems", {})
    if not package_SpecialService_obj:
        package_service_type = list()
        dangerousGoods_accessibility = ""
    else:
        for package_SpecialService_item in package_SpecialService_obj:
            package_SpecialService_array = package_SpecialService_item.get("packageSpecialServices",{})
            if not package_SpecialService_array:
                package_service_type = list()
                dangerousGoods_accessibility = ""
            else:
                temp_special_service = clean_special_service(package_SpecialService_array.get('specialServiceTypes',{}))
                if temp_special_service:
                    package_service_type.extend(temp_special_service)

                temp_dangerousGoodsDetail = package_SpecialService_array.get('dangerousGoodsDetail',{})
                if temp_dangerousGoodsDetail:
                    dangerousGoods_accessibility = temp_dangerousGoodsDetail.get("accessibility", "")

                signatureOptionType = package_SpecialService_array.get('signatureOptionType',{})

    if package_service_type:
        package_service_type = list(set(package_service_type))
        if dangerousGoods_accessibility:
            package_service_type = append_DG(package_service_type, dangerousGoods_accessibility)
        if signatureOptionType:
            package_service_type = append_SignOption(package_service_type, signatureOptionType)

        temp_package_specialServiceType = ", ".join(package_service_type)
    else:
        temp_package_specialServiceType = ""
        package_service_type = list()

    labelResponseOptions = inner_json.get('labelResponseOptions',  "")
    # shipAction = inner_json.get('shipAction',  "")
    # processingOptionType = inner_json.get('processingOptionType',  "")
    # oneLabelAtATime = inner_json.get('oneLabelAtATime',  "")

    shippingChargesPayment = inner_json["requestedShipment"]['shippingChargesPayment']
    paymentType_shippingChargesPayment = shippingChargesPayment.get("paymentType",  "")

    customsClearanceDetail = inner_json["requestedShipment"].get("customsClearanceDetail",  "")
    if customsClearanceDetail:
        dutiesPayment_obj = customsClearanceDetail.get("dutiesPayment",  "")
        if dutiesPayment_obj:
            paymentTypeDutiesPaymentCustomsClearanceDetail = dutiesPayment_obj.get("paymentType", "")
        else:
            paymentTypeDutiesPaymentCustomsClearanceDetail = ''
    else:
        paymentTypeDutiesPaymentCustomsClearanceDetail = ''

    label_tot = f'{image_type}, {labelStock_type}, {labelResponseOptions}'
    label_tot = label_tot.strip()
    OUTPUT_LIST.append({"Number": Number, "Key": Key, "request_type": request_type, "Region": region,
                        "Name": Name,
                        "Origin_cntry_cd": Origin_cntry_cd,
                        "Destination_cntry_cd": Destination_cntry_cd,
                        "service_typ": service_typ,
                        "packaging_type": packaging_type,
                        # "pickup_type": pickup_type,
                        # "image_type": image_type,
                        # "labelStock_type": labelStock_type,
                        # "labelResponseOptions": labelResponseOptions,
                        "Label_info": label_tot,
                        # "shipAction": shipAction,
                        # "processingOptionType": processingOptionType,
                        "paymentType_shippingChargesPayment": paymentType_shippingChargesPayment,
                        "paymentType_dutiesPayment_customsClearanceDetail": paymentTypeDutiesPaymentCustomsClearanceDetail,
                        # "oneLabelAtATime": oneLabelAtATime,
                        # "dangerousGoods_accessibility": dangerousGoods_accessibility,
                        "shipment_specialServiceType": temp_shipment_specialServiceType,
                        "package_specialServiceType": temp_package_specialServiceType
                        # ,"Json_Request": inner_json
                        })
    COUNTER += 1
    return None


with (open(INPUT_FILE_NAME, 'r') as input_file_handler, open(OUTPUT_FILE_NAME, 'w') as csvfile):
    data = json.load(input_file_handler)
    for type_of_shipment in data["item"]:
        typeOfReq_cnt += 1
        type_of_request = type_of_shipment.get("name", "")
        print(f"{typeOfReq_cnt}. Type of request:", type_of_request)

        for regions_or_name in type_of_shipment["item"]:
            temp_var = regions_or_name.get("name", "")

            if type_of_request == "Create Shipment":
                region = temp_var
                print(f"\t\t Region: {region}")

                region_based_folder = regions_or_name["item"]
                for individual_request in region_based_folder:
                    if LIMITED_MODE:
                        if COUNTER < 51:
                            print(Name)
                        else:
                            continue

                    individual_request_name = individual_request["name"]
                    # print("\t\t\tRequest Name:", individual_request_name)
                    request_name.append(individual_request_name)
                    try:
                        whole_request = individual_request['request']['body']['raw']
                    except Exception as e:
                        print(" $$$$$$$$$$$$$  ABEND $$$$$$$$$$$$$")
                        print("An unexpected error: ", e)
                        print("Request name:", individual_request_name)
                        print("Region:", region_based_folder)
                        quit()

                    # if searched_text in whole_request:
                    # if region == 'International':
                    if 1:
                        # print("\t\t\t\t Matched", individual_request_name)
                        matched_list.append(individual_request_name)
                        create_output_from_json(whole_request, individual_request_name, type_of_request, region)

                        package_service_type = list()
                        shipment_service_type = list()
                    region_based_count += 1

                # print(f"\t\t {region}'s count: {region_based_count}")
                create_shipment_tally[region] = region_based_count
                region_based_count = 0

            else:
                newline_position = temp_var.find('\n')
                if newline_position != -1:
                    # print("Problem text:", temp_var)
                    # Problem text: Create Tag for Domestic US Express  for recipient residential address & for type of pickup to contact FedEx.
                    individual_request_name = temp_var[:newline_position]
                    newline_position = -1
                else:
                    individual_request_name = temp_var

                request_name.append(individual_request_name)

                whole_request = regions_or_name['request']['body']['raw']
                if searched_text in whole_request:
                    matched_list.append(individual_request_name)
                other_req_tally[type_of_request] = other_req_tally.get(type_of_request, 0) + 1

                if type_of_request == "Validate Shipment":
                    create_output_from_json(whole_request, individual_request_name, type_of_request, "")
                else:
                    # Name = replace_special_characters_with_underscore(individual_request_name)
                    # Name = Key + "_" + Name

                    has_key_already_assigned = False
                    if (individual_request_name.startswith('SH') and individual_request_name[2:6].isdigit() and
                            individual_request_name[6:7] == '_'):
                        has_key_already_assigned = True

                    Key = generate_key(type_of_request, '')
                    # Number = COUNTER
                    Number = int(Key[2:])
                    Name = replace_special_characters_with_underscore(individual_request_name)
                    if not has_key_already_assigned:
                        new_request_cnt = new_request_cnt + 1
                        Name = Key + "_" + Name
                        print(f"{new_request_cnt}. {Name}")
                    # below is for debugging if there are any other issues
                    else:
                        if (individual_request_name[7:9] == 'SH' and individual_request_name[9:13].isdigit()
                                and individual_request_name[13:14] == '_'):
                            print("Problem request $$$$$$: ",individual_request_name)

                    OUTPUT_LIST.append({"Number": Number, "Key": Key, "request_type": type_of_request, "Region": "", "Name": Name,
                                        "Origin_cntry_cd": "", "Destination_cntry_cd": "",
                                        "service_typ": "",
                                        "packaging_type": "",
                                        # "pickup_type": "",
                                        # "image_type": "",
                                        # "labelStock_type": "",
                                        # "labelResponseOptions": "",
                                        "Label_info": "",
                                        # "shipAction": "",
                                        # "processingOptionType": "",
                                        "paymentType_shippingChargesPayment": "",
                                        "paymentType_dutiesPayment_customsClearanceDetail": "",
                                        # "oneLabelAtATime": "",
                                        # "dangerousGoods_accessibility": "",
                                        "shipment_specialServiceType": "",
                                        "package_specialServiceType": ""
                                        # ,"Json_Request": inner_json
                                        })
                    COUNTER += 1

    "sorting order of input data"
    SORTED_LST = sorted(OUTPUT_LIST, key=lambda J: J["Number"])

    """
    This is a place wherein you write into the output file
    """
    dict_writer_obj = csv.DictWriter(csvfile, fieldnames=headers, delimiter=DELIMITER, restval='NA',
                                     extrasaction='raise', quoting=csv.QUOTE_NONE, escapechar="~")
    # optional - write a header row
    dict_writer_obj.writeheader()

    # write all rows from list to file
    dict_writer_obj.writerows(SORTED_LST)


# Define the SQL statement for bulk insert
sql = '''INSERT INTO SHIPMENT (
    Number,
    Key,
    Request_type,
    Region,
    Name,
    Origin_cntry_cd,
    Destination_cntry_cd,
    service_typ,
    packaging_type,
    Label_type,
    paymentType_shippingChargesPayment,
    paymentType_dutiesPayment_customsClearanceDetail,
    shipment_specialServiceType,
    package_specialServiceType)

    VALUES(
    :Number,
    :Key,
    :request_type,
    :Region,
    :Name,
    :Origin_cntry_cd,
    :Destination_cntry_cd,
    :service_typ,
    :packaging_type,
    :Label_info,
    :paymentType_shippingChargesPayment,
    :paymentType_dutiesPayment_customsClearanceDetail,
    :shipment_specialServiceType,
    :package_specialServiceType )'''


# Execute the bulk insert
cursor.executemany(sql, SORTED_LST)

# Commit the transaction
connection.commit()

# closing the cursor
cursor.close()

"""
Below is summary statics
"""

print('@' * 40)
print('Create shipment stats: ')
for k, v in create_shipment_tally.items():
    print(f"{k:24s} :", v)

print('$' * 40)
print('Other shipment stats: ')
for k, v in other_req_tally.items():
    print(f"{k:24s} :", v)

print(f" Total Unique requests : {len(request_name)} ")
