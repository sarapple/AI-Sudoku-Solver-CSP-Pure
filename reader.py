class Reader:
  @staticmethod
  def read(input_file_name):
    f = open(input_file_name, "r")
    full_page = f.read()

    if full_page == '':
      return []

    rows = [row for row in full_page.split("\n") if row != '']
  
    return rows
