from .base import FunctionalTest
from unittest import skip
 
        
class ItemValidationTest(FunctionalTest):
    
    
    @skip
    def test_cannot_add_empty_list_items(self):
        # 彤彤前往首頁，一不小心按下ENTER鍵，送出了一個空的項目
        
        # 頁面更新，出現一個錯誤訊息：項目不能空白
        
        # 她再試一次，輸入文字，這次運作良好
        
        # 她頑皮地又輸入了一次空白項目
        
        # 她還是看到了同樣的錯誤訊息
        
        # 她可以輸入文字來更正錯誤
        self.fail('填資料吧!')