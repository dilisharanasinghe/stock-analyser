import investpy

TURNOVER_LIMIT = 1000000.0


def search(name):
    try:
        search_result = investpy.search_quotes(text=name, products=['stocks'],
                                               countries=['sri lanka'], n_results=1)
        print(search_result)
        # technical_indicators = search_result.retrieve_technical_indicators(interval="daily")
        # print(technical_indicators)
        information = search_result.retrieve_information()
        print(information)
    except Exception:
        pass


if __name__ == '__main__':
    with open('listed-company.csv', 'r') as f:
        lines = f.read().split('\n')

    all = {}

    for line in lines:
        try:
            data = line.split(',')
            all[data[1]] = data[2].split('.')[0]
        except ValueError:
            pass
        except IndexError:
            pass

    print(all)
    print(len(all))
    print(str(all.values()))