from parser import Parser
from html_saver import HtmlSaver


def run_test():
    parser = Parser(html_saver=HtmlSaver(pagination_limit=5), upd_indexes=True)
    parser.prep_csv_file()
    parser.collect_data()
    parser.convert_csv_to_xlsx('result.csv', 'res_xlsx.xlsx')


def run():
    parser = Parser(html_saver=HtmlSaver(),
                    upd_indexes=False)
    parser.prep_csv_file()
    parser.collect_data()
    parser.convert_csv_to_xlsx('result.csv', 'res_xlsx.xlsx')


if __name__ == "__main__":
    # run_test()
    run()



