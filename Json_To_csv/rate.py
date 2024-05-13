import json
import csv
import re

'''
This Module is Json to csv converter for Rating & comprehensive Rating requests. It also stores data in database.
Extract: A complex Json collection: This collections contains multiple JSON requests. Each requests has multiple objects, arrays and key-value pairs
Transform: There is a business logic keyed in 
Load: CSV file for selected data
'''

DELIMITER = '|'

INPUT_FILE_NAME = '/Users/kalpandalal/IdeaProjects/p4ye/Searching_tool/Nandi/Rates and Transit Times APIResponse JSONApiCollection DT05082022.json'

OUTPUT_FILE_NAME = '../output/Rate1_with_orig_name.csv'
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
temp_var = None

headers = ['Number', 'Key', 'request_type', 'Region', 'Name', 'Origin_cntry_cd', 'Destination_cntry_cd', 'service_typ',
           'packaging_type',
           # 'pickup_type',
           # 'Label_info',
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

overall_rate_counter = 0

# Comprehensive Rate related counters
US_domestic_cnt = 0
csp_US_cnt = 3000
csp_CA_cnt = 5000
csp_EU_cnt = 6000
csp_LAC_cnt = 7000
csp_APAC_cnt = 8000
other_cnt = 9000

# Rate related counters
US_Domestic_Cnt = 0
Intra_Canada_Cnt = 2000
Intra_Europe_Cnt = 4000
International_Cnt = 6000
Non_US_Domestic_Cnt = 8000

def generate_key(request_type: str, region: str, req_identifier: str) -> str:
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
    :param region: Comprehensive rate sends region while rate api sends value `rate` as identification
    :return:
    """
    global  csp_EU_cnt, csp_LAC_cnt, csp_APAC_cnt, csp_CA_cnt, csp_US_cnt, US_domestic_cnt, other_cnt, \
        US_Domestic_Cnt, Intra_Canada_Cnt, Intra_Europe_Cnt, International_Cnt, Non_US_Domestic_Cnt
    if req_identifier == "Comprehensive Rate":
        match request_type:
            case "CSP":
                if region == 'US':
                    csp_US_cnt += 1
                    return f"RT{csp_US_cnt}"
                elif region == 'EU':
                    csp_EU_cnt += 1
                    return f"RT{csp_EU_cnt}"
                elif region == 'LAC':
                    csp_LAC_cnt += 1
                    return f"RT{csp_LAC_cnt}"
                elif region == 'APAC':
                    csp_APAC_cnt += 1
                    return f"RT{csp_APAC_cnt}"
                elif region == 'CA':
                    csp_CA_cnt += 1
                    return f"RT{csp_CA_cnt}"
                else:
                    print("Request type:", request_type)
                    print("region:", region)
                    raise ValueError("Cannot find valid Request Type")
            case "US Domestic":
                US_domestic_cnt += 1
                return f"RT{US_domestic_cnt:04d}"
            case "Others":
                other_cnt += 1
                return f"RT{other_cnt}"
            case _:
                print("Request type", request_type)
                raise ValueError("Cannot find valid Request Type")
    elif req_identifier == "Rate":
        match request_type:
            case "US Domestic":
                US_Domestic_Cnt += 1
                return f"RT{US_Domestic_Cnt:04d}"
            case "Intra Canada":
                Intra_Canada_Cnt += 1
                return f"RT{Intra_Canada_Cnt:04d}"
            case "Intra Europe":
                Intra_Europe_Cnt += 1
                return f"RT{Intra_Europe_Cnt:04d}"
            case "International":
                International_Cnt += 1
                return f"RT{International_Cnt:04d}"
            case "Non-US Domestic":
                Non_US_Domestic_Cnt += 1
                return f"RT{Non_US_Domestic_Cnt:04d}"
            case "Others":
                other_cnt += 1
                return f"RT{other_cnt}"
            case _:
                print("Request type", request_type)
                raise ValueError("Cannot find valid Request Type")
    else:
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

    #  replace ZWSP with single underscore "_"
    text = text.translate({ord('\u200b'): '_'})

    #  replace multiple spaces " " or "   " with single underscore "_"
    text = re.sub(r'\s+', '_', text)

    #  replace multiple underscores "__" or "___" with single underscore "_"
    text = re.sub(r'_+', '_', text)

    # remove leading or trailing spaces
    interim_text = text.strip()

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


def create_output_from_json(raw_json: str, individual_request_name: str, request_type: str, region: str = '', req_identifier: str = "") -> None:
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
    global COUNTER, OUTPUT_LIST, new_request_cnt, overall_rate_counter
    inner_json = None
    try:
        inner_json = json.loads(raw_json)
    except ValueError as ve:
        print(" !!!!!!!!!!!!!!!!  ABEND !!!!!!!!!!!!!!!!")
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
    Key = 0
    Key = generate_key(request_type, region, req_identifier)
    Number = overall_rate_counter
    Name = replace_special_characters_with_underscore(individual_request_name)
    # Name = individual_request_name

    if not has_key_already_assigned:
        new_request_cnt = new_request_cnt + 1
        Name = Key + "_" + Name
        # print(f"\t\tAfter: {new_request_cnt}. {Name}")
    # below is for debugging if there are any other issues
    else:
        if (individual_request_name[7:9] == 'SH' and individual_request_name[9:13].isdigit()
                and individual_request_name[13:14] == '_'):
            print("Problem request $$$$$$: ", individual_request_name)

    Origin_cntry_cd = inner_json["requestedShipment"]["shipper"]["address"].get("countryCode", "")
    Destination_cntry_cd = inner_json["requestedShipment"]["recipient"]["address"].get("countryCode", "")
    service_typ = inner_json["requestedShipment"].get('serviceType', None)

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

    # labelResponseOptions = inner_json.get('labelResponseOptions',  "")
    # shipAction = inner_json.get('shipAction',  "")
    # processingOptionType = inner_json.get('processingOptionType',  "")
    # oneLabelAtATime = inner_json.get('oneLabelAtATime',  "")

    shippingChargesPayment = inner_json["requestedShipment"].get('shippingChargesPayment', None)
    if shippingChargesPayment is None:
        paymentType_shippingChargesPayment = ''
    else:
        paymentType_shippingChargesPayment = shippingChargesPayment.get("paymentType",  "")
        # print("paymentType_shippingChargesPayment:" , paymentType_shippingChargesPayment)

    customsClearanceDetail = inner_json["requestedShipment"].get("customsClearanceDetail",  "")
    if customsClearanceDetail:
        dutiesPayment_obj = customsClearanceDetail.get("dutiesPayment",  "")
        if dutiesPayment_obj:
            paymentTypeDutiesPaymentCustomsClearanceDetail = dutiesPayment_obj.get("paymentType", "")
            # print('paymentTypeDutiesPaymentCustomsClearanceDetail:', paymentTypeDutiesPaymentCustomsClearanceDetail)
        else:
            paymentTypeDutiesPaymentCustomsClearanceDetail = ''
    else:
        paymentTypeDutiesPaymentCustomsClearanceDetail = ''

    # label_tot = f'{image_type}, {labelStock_type}, {labelResponseOptions}'
    # label_tot = label_tot.strip()


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
                        # "Label_info": label_tot,
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

    # here we have rate API processing
    if data['info']['name'] == 'Rates and Transit Times API':
        data = data['item'][0]

        for grand_parent_folder in data["item"]:
            parent_folder_name = grand_parent_folder['name']
            # print("Folder Name: ", parent_folder_name)

            for request_obj in grand_parent_folder['item']:
                individual_request_name = request_obj['name']
                # print("\tRate Request: ", individual_request_name)
                typeOfReq_cnt += 1
                overall_rate_counter += 1
                whole_request = None
                try:
                    whole_request = request_obj['request']['body']['raw']
                except Exception as e:
                    print(" $$$$$$$$$$$$$ -ABEND-")
                    print("An unexpected error: ", e)
                    print("Request name:", individual_request_name)
                    print(whole_request)
                    quit()

                package_service_type = list()
                shipment_service_type = list()
                create_output_from_json(whole_request, individual_request_name, parent_folder_name, '', "Rate")

        temp_var = grand_parent_folder.get("name", "")
        #  Checking Outer folder name
        if temp_var and temp_var == 'Comprehensive Rates and Transit Time':

            for parent_folder in grand_parent_folder["item"]:
                parent_folder_name = parent_folder["name"]

                #  below if loop is for direct requests
                if parent_folder_name in ["Others", "US Domestic"]:
                    region = parent_folder_name
                    # print(f"Inside folder: {parent_folder_name}")

                    for request_obj in parent_folder["item"]:
                        individual_request_name = request_obj["name"]
                        overall_rate_counter += 1
                        # print(f"\t{overall_rate_counter}. Request Name:", individual_request_name)
                        if individual_request_name == 'Negative-AE-AE CONTACT_FEDEX_TO_SCHEDULE YOUR_PACKAGING LIST_ACCOUNT  ReturnTransitTimes-true  Commodity':
                            print('Here you go.')
                        request_name.append(individual_request_name)

                        try:
                            whole_request = request_obj['request']['body']['raw']
                        except Exception as e:
                            print(" $$$$$$$$$$$$$  ABEND $$$$$$$$$$$$$")
                            print("An unexpected error: ", e)
                            # print("Request name:", individual_request_name)
                            quit()

                        if whole_request is None:
                            print(f"@@@@@@@@@@@@@@@@@ Inside folder: {parent_folder_name}", individual_request_name)

                        create_output_from_json(whole_request, individual_request_name, parent_folder_name, "Rate", "Comprehensive Rate")
                        package_service_type = list()
                        shipment_service_type = list()

                        # region_based_count += 1
                        # create_shipment_tally[region] = region_based_count
                        # region_based_count = 0

                #  below elif loop is for region based folder;; hence, there will be extra for loop
                elif parent_folder_name == 'CSP':
                    for region in parent_folder['item']:
                        region_name = region.get("name", "")
                        print("\t\t", region_name)

                        for request_obj in region["item"]:
                            individual_request_name = request_obj["name"]
                            overall_rate_counter += 1
                            # print(f"\t{overall_rate_counter}. Request Name:", individual_request_name)
                            request_name.append(individual_request_name)

                            try:
                                whole_request = request_obj['request']['body']['raw']
                            except Exception as e:
                                print("@@@@@@@@@@@@@@  ABEND @@@@@@@@@@@@@@")
                                print("An unexpected error: ", e)
                                print("Request name:", individual_request_name)
                                quit()

                            create_output_from_json(whole_request, individual_request_name, parent_folder_name,
                                                    region_name, "Comprehensive Rate")

                            package_service_type = list()
                            shipment_service_type = list()

    "sorting order of input data"
    SORTED_LST = sorted(OUTPUT_LIST, key=lambda J: int(J["Key"][2:]) if J["Key"] else 395)


    '''
    Unit testing
    '''
    for record in SORTED_LST:
        name_of_req = record["Name"]
        num_of_spaces = name_of_req.count(" ")
        '1) checks if any spaces are pending in the name '
        if num_of_spaces > 0:
            print('@@@@@@@@@@@@@')
            print("Full record: ", record)
            print("num_of_spacess:", num_of_spaces)
        '2) checks preceding or leading underscore'
        if name_of_req.endswith("_") or name_of_req.startswith("_"):
            print('@@@@@@@@@@@@@')
            print("Full record: ", record)
        '3) checking if name already has numbers'
        if name_of_req[7:13].isdigit():
            print(name_of_req)

    """
    This is a place wherein you write into the output file
    """
    dict_writer_obj = csv.DictWriter(csvfile, fieldnames=headers, delimiter=DELIMITER, restval='NA',
                                     extrasaction='raise', quoting=csv.QUOTE_NONE, escapechar="~")
    # optional - write a header row
    dict_writer_obj.writeheader()

    # write all rows from list to file
    dict_writer_obj.writerows(SORTED_LST)

# """
# Below is summary statics
# """
#
# print('@' * 40)
# print('RATE shipment stats: ')
# for k, v in create_shipment_tally.items():
#     print(f"{k:24s} :", v)
#
# print('$' * 40)
# print('Other shipment stats: ')
# for k, v in other_req_tally.items():
#     print(f"{k:24s} :", v)
#
# print(f" Total Unique requests : {len(request_name)} ")
