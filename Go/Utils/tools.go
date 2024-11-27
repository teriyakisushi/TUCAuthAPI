package tools

import (
    "errors"
    "fmt"
    "io/ioutil"
    "os"
)

// Tools struct
type Tools struct{}

// 保存请求文本到本地
func (t *Tools) SaveResponseText(resTxt string, fileName string, savePath string) error {
    if resTxt == "" || fileName == "" {
        return errors.New("请求文本或文件名不能为空！")
    }

    if savePath == "" {
        savePath = "./Response"
    }

    err := os.MkdirAll(savePath, os.ModePerm)
    if err != nil {
        return err
    }

    filePath := savePath + "/" + fileName
    err = ioutil.WriteFile(filePath, []byte(resTxt), 0644)
    if err != nil {
        return err
    }

    fmt.Printf("Save the request text to %s successfully!\n", filePath)
    return nil
}

// 解析课程表的json数据
func (t *Tools) UrpCourseInfoParse(source string, isFile bool) (map[string]interface{}, error) {
    if source == "" {
        return nil, errors.New("请求文本或文件路径不能为空！")
    }

    if isFile {
        data, err := ioutil.ReadFile(source)
        if err != nil {
            return nil, err
        }
        source = string(data)
    }

    // var result map[string]interface{}
    // err := json.Unmarshal([]byte(source), &result)
    // if err != nil {
    //     return nil, err
    // }

    // return result, nil
    return nil, nil
}

// BytesToImg 将字节流数据保存为图片
func (t *Tools) BytesToImg(byteData []byte, imgPath string) error {
    err := ioutil.WriteFile(imgPath, byteData, 0644)
    if err != nil {
        return err
    }

    fmt.Printf("Save the image to %s successfully!\n", imgPath)
    return nil
}