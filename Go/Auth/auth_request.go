package auth_request

import (
    "fmt"
    "io/ioutil"
    "log"
    "net/http"
    "regexp"
    "time"

    "github.com/robertkrimen/otto"
    "github.com/playwright-community/playwright-go"
)

type TJCUAuth struct {
    user        string
    pwd         string
    serviceURL  string
    authURL     string
    Referer     string
    loginStatus bool
    UA          string
    encrypt     *otto.Otto
    client      *http.Client
}

func NewTJCUAuth(user, pwd, targetURL string) *TJCUAuth {
    vm := otto.New()
    script, err := ioutil.ReadFile("encrypt.js")
    if err != nil {
        log.Fatalf("Failed to read encrypt.js: %v", err)
    }
    _, err = vm.Run(script)
    if err != nil {
        log.Fatalf("Failed to compile encrypt.js: %v", err)
    }

    return &TJCUAuth{
        user:       user,
        pwd:        pwd,
        serviceURL: targetURL,
        authURL:    "http://authserver.tjcu.edu.cn/authserver/login",
        Referer:    "http://authserver.tjcu.edu.cn/authserver/login?service=" + targetURL,
        UA:         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        encrypt:    vm,
        client:     &http.Client{},
    }
}

func (auth *TJCUAuth) getSalt() (string, string, error) {
    req, err := http.NewRequest("GET", auth.authURL, nil)
    if err != nil {
        return "", "", err
    }
    req.Header.Set("User-Agent", auth.UA)
    req.Header.Set("Referer", auth.Referer)
    q := req.URL.Query()
    q.Add("service", auth.serviceURL)
    req.URL.RawQuery = q.Encode()

    resp, err := auth.client.Do(req)
    if err != nil {
        return "", "", err
    }
    defer resp.Body.Close()

    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        return "", "", err
    }

    saltRe := regexp.MustCompile(`pwdDefaultEncryptSalt = "(.*?)";`)
    ltRe := regexp.MustCompile(`input type="hidden" name="lt" value="(.*?)"`)

    salt := saltRe.FindStringSubmatch(string(body))
    lt := ltRe.FindStringSubmatch(string(body))

    if len(salt) < 2 || len(lt) < 2 {
        return "", "", fmt.Errorf("failed to get salt or lt")
    }

    return salt[1], lt[1], nil
}

func (auth *TJCUAuth) login() (string, error) {
    salt, lt, err := auth.getSalt()
    if err != nil {
        return "", err
    }

    pwd, err := auth.encrypt.Call("encryptAES", auth.pwd, salt)
    if err != nil {
        return "", err
    }

    data := url.Values{
        "username": {auth.user},
        "password": {pwd.String()},
        "lt":       {lt},
        "dllt":     {"userNamePasswordLogin"},
        "execution": {"e1s1"},
        "_eventId": {"submit"},
        "rmShown":  {"1"},
    }

    req, err := http.NewRequest("POST", auth.authURL, strings.NewReader(data.Encode()))
    if err != nil {
        return "", err
    }
    req.Header.Set("User-Agent", auth.UA)
    req.Header.Set("Referer", auth.Referer)
    req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

    resp, err := auth.client.Do(req)
    if err != nil {
        return "", err
    }
    defer resp.Body.Close()

    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        return "", err
    }

    if strings.Contains(string(body), "统一身份认证") {
        return "", fmt.Errorf("登录失败，请检查用户名和密码是否正确")
    }

    auth.loginStatus = true
    return string(body), nil
}

func (auth *TJCUAuth) powerLogin() (string, error) {
    pw, err := playwright.Run()
    if err != nil {
        return "", err
    }
    defer pw.Stop()

    browser, err := pw.Chromium.Launch()
    if err != nil {
        return "", err
    }
    defer browser.Close()

    context, err := browser.NewContext()
    if err != nil {
        return "", err
    }

    page, err := context.NewPage()
    if err != nil {
        return "", err
    }

    page.Goto(auth.authURL + "?service=" + auth.serviceURL)
    page.WaitForLoadState("load")

    if page.Title() == "统一身份认证" {
        page.Fill("input[id='username']", auth.user)
        page.Fill("input[id='password']", auth.pwd)
        time.Sleep(1 * time.Second)
        page.Click("button[type='submit']")

        page.Goto(auth.serviceURL)
        page.WaitForLoadState("load")

        if page.Title() == "统一身份认证" {
            return "", fmt.Errorf("登录失败，请检查用户名和密码是否正确")
        }

        auth.loginStatus = true
    }

    content, err := page.Content()
    if err != nil {
        return "", err
    }

    cookies, err := context.Cookies()
    if err != nil {
        return "", err
    }

    for _, cookie := range cookies {
        auth.client.Jar.SetCookies(auth.authURL, []*http.Cookie{
            {
                Name:  cookie.Name,
                Value: cookie.Value,
                Domain: cookie.Domain,
            },
        })
    }

    return content, nil
}

func (auth *TJCUAuth) cleanCookies() {
    auth.client.Jar, _ = cookiejar.New(nil)
    log.Println("Clean the cookies successfully!")
}

func main() {
    auth := NewTJCUAuth("your_username", "your_password", "your_target_url")
    content, err := auth.login()
    if err != nil {
        log.Fatalf("Login failed: %v", err)
    }
    fmt.Println(content)
}