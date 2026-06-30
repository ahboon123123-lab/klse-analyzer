.class public final Lcom/stub/StubApp;
.super Landroid/app/Application;
.source "SourceFile"


# static fields
.field private static loadFromLib:Z

.field private static needX86Bridge:Z

.field public static strEntryApplication:Ljava/lang/String;

.field private static ᵢˋ:Landroid/app/Application;

.field private static ᵢˎ:Landroid/app/Application;

.field private static ᵢˏ:Ljava/lang/String;

.field private static ᵢˑ:Landroid/content/Context;

.field private static ᵢי:Ljava/lang/String;

.field private static ᵢـ:Ljava/lang/String;

.field private static ᵢٴ:Ljava/lang/String;

.field private static ᵢᐧ:Ljava/lang/String;

.field private static ᵢᴵ:Ljava/lang/String;

.field private static ᵢᵎ:Ljava/util/Map;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/Map",
            "<",
            "Ljava/lang/Integer;",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field


# direct methods
.method static constructor <clinit>()V
    .locals 3

    .prologue
    const/4 v2, 0x0

    const/4 v1, 0x0

    .line 31
    sput-object v1, Lcom/stub/StubApp;->ᵢˋ:Landroid/app/Application;

    .line 32
    const-string v0, "entryRunApplication"

    sput-object v0, Lcom/stub/StubApp;->strEntryApplication:Ljava/lang/String;

    .line 33
    sput-object v1, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;

    .line 34
    const-string v0, "libjiagu"

    sput-object v0, Lcom/stub/StubApp;->ᵢˏ:Ljava/lang/String;

    .line 35
    const/4 v2, 0x0

    sput-boolean v2, Lcom/stub/StubApp;->loadFromLib:Z

    .line 36
    const/4 v2, 0x0

    sput-boolean v2, Lcom/stub/StubApp;->needX86Bridge:Z

    .line 39
    sput-object v1, Lcom/stub/StubApp;->ᵢי:Ljava/lang/String;

    .line 40
    sput-object v1, Lcom/stub/StubApp;->ᵢـ:Ljava/lang/String;

    .line 41
    sput-object v1, Lcom/stub/StubApp;->ᵢٴ:Ljava/lang/String;

    .line 42
    sput-object v1, Lcom/stub/StubApp;->ᵢᐧ:Ljava/lang/String;

    .line 43
    sput-object v1, Lcom/stub/StubApp;->ᵢᴵ:Ljava/lang/String;

    .line 44
    new-instance v0, Ljava/util/concurrent/ConcurrentHashMap;

    invoke-direct {v0}, Ljava/util/concurrent/ConcurrentHashMap;-><init>()V

    sput-object v0, Lcom/stub/StubApp;->ᵢᵎ:Ljava/util/Map;

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 30
    invoke-direct {p0}, Landroid/app/Application;-><init>()V

    return-void
.end method

.method public static getAppContext()Landroid/content/Context;
    .locals 1

    .prologue
    .line 61
    sget-object v0, Lcom/stub/StubApp;->ᵢˑ:Landroid/content/Context;

    return-object v0
.end method

.method public static getDir()Ljava/lang/String;
    .locals 1

    .prologue
    .line 57
    sget-object v0, Lcom/stub/StubApp;->ᵢᐧ:Ljava/lang/String;

    return-object v0
.end method

.method public static getOrigApplicationContext(Landroid/content/Context;)Landroid/content/Context;
    .locals 1

    .prologue
    .line 65
    sget-object v0, Lcom/stub/StubApp;->ᵢˋ:Landroid/app/Application;

    if-ne p0, v0, :cond_0

    .line 66
    sget-object p0, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;

    .line 68
    :cond_0
    return-object p0
.end method

.method public static getSoPath1()Ljava/lang/String;
    .locals 1

    .prologue
    .line 49
    sget-object v0, Lcom/stub/StubApp;->ᵢـ:Ljava/lang/String;

    return-object v0
.end method

.method public static getSoPath2()Ljava/lang/String;
    .locals 1

    .prologue
    .line 53
    sget-object v0, Lcom/stub/StubApp;->ᵢٴ:Ljava/lang/String;

    return-object v0
.end method

.method public static getString2(I)Ljava/lang/String;
    .locals 3

    .prologue
    .line 263
    sget-object v0, Lcom/stub/StubApp;->ᵢᵎ:Ljava/util/Map;

    invoke-static {p0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v1

    invoke-interface {v0, v1}, Ljava/util/Map;->get(Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/String;

    .line 264
    if-nez v0, :cond_0

    .line 265
    invoke-static {p0}, Lcom/stub/StubApp;->interface14(I)Ljava/lang/String;

    move-result-object v0

    .line 266
    sget-object v1, Lcom/stub/StubApp;->ᵢᵎ:Ljava/util/Map;

    invoke-static {p0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v2

    invoke-interface {v1, v2, v0}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;

    .line 268
    :cond_0
    if-eqz v0, :cond_1

    .line 269
    invoke-virtual {v0}, Ljava/lang/String;->intern()Ljava/lang/String;

    move-result-object v0

    .line 271
    :cond_1
    return-object v0
.end method

.method public static getString2(Ljava/lang/String;)Ljava/lang/String;
    .locals 1

    .prologue
    .line 276
    :try_start_0
    invoke-static {p0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v0

    .line 277
    invoke-static {v0}, Lcom/stub/StubApp;->getString2(I)Ljava/lang/String;
    :try_end_0
    .catch Ljava/lang/NumberFormatException; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object v0

    .line 281
    :goto_0
    return-object v0

    .line 278
    :catch_0
    move-exception v0

    .line 279
    invoke-virtual {v0}, Ljava/lang/NumberFormatException;->printStackTrace()V

    .line 281
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public static native interface11(I)V
.end method

.method public static native interface12(Ldalvik/system/DexFile;)Ljava/util/Enumeration;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ldalvik/system/DexFile;",
            ")",
            "Ljava/util/Enumeration",
            "<",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end method

.method public static native interface13(IJJJIIJ)J
.end method

.method public static native interface14(I)Ljava/lang/String;
.end method

.method public static native interface17(Landroid/content/res/AssetManager;Ljava/lang/String;)Landroid/content/res/AssetFileDescriptor;
.end method

.method public static native interface18(Ljava/lang/Class;Ljava/lang/String;)Ljava/io/InputStream;
.end method

.method public static native interface19(Ljava/lang/ClassLoader;Ljava/lang/String;)Ljava/io/InputStream;
.end method

.method public static native interface20()V
.end method

.method public static native interface21(Landroid/app/Application;)V
.end method

.method public static native interface22(I[Ljava/lang/String;[I)V
.end method

.method public static native interface5(Landroid/app/Application;)V
.end method

.method public static native interface6(Ljava/lang/String;)Ljava/lang/String;
.end method

.method public static native interface7(Landroid/app/Application;Landroid/content/Context;)Z
.end method

.method public static native interface8(Landroid/app/Application;Landroid/content/Context;)Z
.end method

.method public static native mark(Landroid/location/LocationManager;Ljava/lang/String;)Landroid/location/Location;
.end method

.method public static native mark()V
.end method

.method public static native mark(Landroid/location/Location;)V
.end method

.method public static native declared-synchronized n0101()Z
.end method

.method public static native declared-synchronized n01030(Ljava/lang/Object;)V
.end method

.method public static native declared-synchronized n01033(Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native declared-synchronized n010333(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0110()V
.end method

.method public static native n0111()I
.end method

.method public static native n01110(Z)V
.end method

.method public static native n01111(Z)I
.end method

.method public static native n011110(ZI)V
.end method

.method public static native n011111(II)I
.end method

.method public static native n0111111(IZZ)I
.end method

.method public static native n01111111(BBBB)I
.end method

.method public static native n011111113(ZIIBB)Ljava/lang/Object;
.end method

.method public static native n0111111131(IIIIILjava/lang/Object;)I
.end method

.method public static native n011111131(CCZILjava/lang/Object;)Z
.end method

.method public static native n0111112(III)J
.end method

.method public static native n01111133(BBBLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011112(II)D
.end method

.method public static native n011113(BB)Ljava/lang/Object;
.end method

.method public static native n0111131(IILjava/lang/Object;)I
.end method

.method public static native n0111131331(ZZLjava/lang/Object;ZLjava/lang/Object;Ljava/lang/Object;)Z
.end method

.method public static native n01111313331(ZZLjava/lang/Object;ZLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Z
.end method

.method public static native n0111133(IILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011113313133(ZZLjava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0111133133(ZZLjava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01112(I)J
.end method

.method public static native n011120(IJ)V
.end method

.method public static native n011121(BJ)I
.end method

.method public static native n0111211(IJI)I
.end method

.method public static native n01112111(IJII)I
.end method

.method public static native n0111211111(IJIIII)I
.end method

.method public static native n01112113(IJII)Ljava/lang/Object;
.end method

.method public static native n01112113111(IJIILjava/lang/Object;II)I
.end method

.method public static native n0111212(IJI)J
.end method

.method public static native n01112121111(IJIJIII)I
.end method

.method public static native n011121221(IJIJJ)I
.end method

.method public static native n0111213111(IJILjava/lang/Object;II)I
.end method

.method public static native n011122(BJ)J
.end method

.method public static native n0111222(FDD)D
.end method

.method public static native n01112231(IJJLjava/lang/Object;)I
.end method

.method public static native n01112233(IJJLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0111231(IJLjava/lang/Object;)I
.end method

.method public static native n0111233(IJLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01113(I)Ljava/lang/Object;
.end method

.method public static native n011130(ILjava/lang/Object;)V
.end method

.method public static native n011131(ILjava/lang/Object;)I
.end method

.method public static native n01113111(ILjava/lang/Object;II)I
.end method

.method public static native n011131122(ILjava/lang/Object;IIJ)J
.end method

.method public static native n01113113(ILjava/lang/Object;II)Ljava/lang/Object;
.end method

.method public static native n01113113111(ILjava/lang/Object;IILjava/lang/Object;II)I
.end method

.method public static native n0111313(ILjava/lang/Object;Z)Ljava/lang/Object;
.end method

.method public static native n01113130(ILjava/lang/Object;ILjava/lang/Object;)V
.end method

.method public static native n011132(ILjava/lang/Object;)D
.end method

.method public static native n011132222(ILjava/lang/Object;JJJ)J
.end method

.method public static native n011133(ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0111330(ILjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public static native n0111331(ILjava/lang/Object;Ljava/lang/Object;)I
.end method

.method public static native n0111333(ILjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01113330(ILjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public static native n011133331(ILjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)I
.end method

.method public static native n011133333(ILjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0112()J
.end method

.method public static native n01120(J)V
.end method

.method public static native n01121(J)I
.end method

.method public static native n011210(JI)V
.end method

.method public static native n011211(JI)I
.end method

.method public static native n0112111(JII)I
.end method

.method public static native n011211110(JISSI)V
.end method

.method public static native n011211213(JIIJZ)Ljava/lang/Object;
.end method

.method public static native n01121123(JIIJ)Ljava/lang/Object;
.end method

.method public static native n0112113330(JIILjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public static native n011212(JI)J
.end method

.method public static native n011212210(JIJJZ)V
.end method

.method public static native n011212310(JIJLjava/lang/Object;Z)V
.end method

.method public static native n011213(JI)Ljava/lang/Object;
.end method

.method public static native n0112130(JZLjava/lang/Object;)V
.end method

.method public static native n01121310(JBLjava/lang/Object;I)V
.end method

.method public static native n0112132(JILjava/lang/Object;)J
.end method

.method public static native n01122(J)J
.end method

.method public static native n011220(JJ)V
.end method

.method public static native n011221(JJ)Z
.end method

.method public static native n0112210(JJZ)V
.end method

.method public static native n01122112121111111212122(JJIIJIJIFIFIFIDIDID)J
.end method

.method public static native n011221121212122(JJIIJIJIJIJ)J
.end method

.method public static native n01122113(DDII)Ljava/lang/Object;
.end method

.method public static native n0112211313131312121211111111122(JJIILjava/lang/Object;ILjava/lang/Object;ILjava/lang/Object;ILjava/lang/Object;IJIJIJIIIIIIIFID)J
.end method

.method public static native n011221131313131313132(JJIILjava/lang/Object;ILjava/lang/Object;ILjava/lang/Object;ILjava/lang/Object;ILjava/lang/Object;ILjava/lang/Object;ILjava/lang/Object;)J
.end method

.method public static native n011221131313132(JJIILjava/lang/Object;ILjava/lang/Object;ILjava/lang/Object;ILjava/lang/Object;)J
.end method

.method public static native n0112213(JJB)Ljava/lang/Object;
.end method

.method public static native n01122130(JJILjava/lang/Object;)V
.end method

.method public static native n011222(JJ)J
.end method

.method public static native n0112220(JJJ)V
.end method

.method public static native n01122210(JJJZ)V
.end method

.method public static native n011222110(JJJZZ)V
.end method

.method public static native n011222112(JJJZZ)J
.end method

.method public static native n0112222(JJJ)J
.end method

.method public static native n01122220(JJJJ)V
.end method

.method public static native n011222210(JJJDZ)V
.end method

.method public static native n011222212(JJJJZ)J
.end method

.method public static native n01122222(JJJJ)J
.end method

.method public static native n0112223(JJJ)Ljava/lang/Object;
.end method

.method public static native n011222310(JJJLjava/lang/Object;Z)V
.end method

.method public static native n01122232(JJJLjava/lang/Object;)J
.end method

.method public static native n011223(JJ)Ljava/lang/Object;
.end method

.method public static native n0112230(JJLjava/lang/Object;)V
.end method

.method public static native n0112232(JJLjava/lang/Object;)J
.end method

.method public static native n0112233(JJLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01122333(JJLjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01123(J)Ljava/lang/Object;
.end method

.method public static native n011230(JLjava/lang/Object;)V
.end method

.method public static native n011231(JLjava/lang/Object;)I
.end method

.method public static native n0112310(JLjava/lang/Object;Z)V
.end method

.method public static native n0112311(JLjava/lang/Object;I)I
.end method

.method public static native n01123111(JLjava/lang/Object;II)I
.end method

.method public static native n011231133(DLjava/lang/Object;IILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0112313(JLjava/lang/Object;I)Ljava/lang/Object;
.end method

.method public static native n01123131(JLjava/lang/Object;ILjava/lang/Object;)I
.end method

.method public static native n01123133(JLjava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011232(JLjava/lang/Object;)J
.end method

.method public static native n0112320(JLjava/lang/Object;D)V
.end method

.method public static native n01123212(JLjava/lang/Object;JZ)J
.end method

.method public static native n0112322212(JLjava/lang/Object;JJJZ)J
.end method

.method public static native n011233(JLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0112330(JLjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public static native n0112331(JLjava/lang/Object;Ljava/lang/Object;)I
.end method

.method public static native n011233112(JLjava/lang/Object;Ljava/lang/Object;ZZ)J
.end method

.method public static native n01123313(JLjava/lang/Object;Ljava/lang/Object;I)Ljava/lang/Object;
.end method

.method public static native n0112332(JLjava/lang/Object;Ljava/lang/Object;)J
.end method

.method public static native n01123320(JLjava/lang/Object;Ljava/lang/Object;J)V
.end method

.method public static native n0112333(JLjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011233331(JLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Z
.end method

.method public static native n011233331133313(JLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ZBLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;B)Ljava/lang/Object;
.end method

.method public static native n0113()Ljava/lang/Object;
.end method

.method public static native n01130(Ljava/lang/Object;)V
.end method

.method public static native n01131(Ljava/lang/Object;)I
.end method

.method public static native n011310(Ljava/lang/Object;I)V
.end method

.method public static native n011311(Ljava/lang/Object;Z)Z
.end method

.method public static native n0113110(Ljava/lang/Object;IB)V
.end method

.method public static native n0113111(Ljava/lang/Object;IC)Z
.end method

.method public static native n01131110(Ljava/lang/Object;BII)V
.end method

.method public static native n01131111(Ljava/lang/Object;BII)I
.end method

.method public static native n011311110(Ljava/lang/Object;IIII)V
.end method

.method public static native n01131111133(Ljava/lang/Object;IIIIILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011311113(Ljava/lang/Object;IIZZ)Ljava/lang/Object;
.end method

.method public static native n0113111130(Ljava/lang/Object;BIIILjava/lang/Object;)V
.end method

.method public static native n0113111131(Ljava/lang/Object;BIIILjava/lang/Object;)I
.end method

.method public static native n0113111133(Ljava/lang/Object;IIZILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01131112(Ljava/lang/Object;IZZ)J
.end method

.method public static native n01131113(Ljava/lang/Object;IIZ)Ljava/lang/Object;
.end method

.method public static native n011311130(Ljava/lang/Object;IIILjava/lang/Object;)V
.end method

.method public static native n01131113133(Ljava/lang/Object;IIZLjava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011311132(Ljava/lang/Object;IIILjava/lang/Object;)J
.end method

.method public static native n011311133(Ljava/lang/Object;IIZLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0113112(Ljava/lang/Object;II)J
.end method

.method public static native n0113113(Ljava/lang/Object;II)Ljava/lang/Object;
.end method

.method public static native n01131130(Ljava/lang/Object;IILjava/lang/Object;)V
.end method

.method public static native n01131131(Ljava/lang/Object;IILjava/lang/Object;)I
.end method

.method public static native n011311311(Ljava/lang/Object;IILjava/lang/Object;I)Z
.end method

.method public static native n0113113111133(Ljava/lang/Object;IILjava/lang/Object;ZZZZLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0113113113(Ljava/lang/Object;IILjava/lang/Object;II)Ljava/lang/Object;
.end method

.method public static native n01131133(Ljava/lang/Object;IILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011312(Ljava/lang/Object;I)J
.end method

.method public static native n0113120(Ljava/lang/Object;IJ)V
.end method

.method public static native n01131223133(Ljava/lang/Object;ZJJLjava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011312233(Ljava/lang/Object;ZJJLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011312333(Ljava/lang/Object;IJLjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011313(Ljava/lang/Object;I)Ljava/lang/Object;
.end method

.method public static native n0113130(Ljava/lang/Object;ILjava/lang/Object;)V
.end method

.method public static native n0113131(Ljava/lang/Object;ILjava/lang/Object;)B
.end method

.method public static native n011313110(Ljava/lang/Object;ILjava/lang/Object;II)V
.end method

.method public static native n011313111(Ljava/lang/Object;ILjava/lang/Object;II)Z
.end method

.method public static native n01131313(Ljava/lang/Object;ILjava/lang/Object;Z)Ljava/lang/Object;
.end method

.method public static native n011313133(Ljava/lang/Object;ILjava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0113132(Ljava/lang/Object;ILjava/lang/Object;)J
.end method

.method public static native n01131323133(Ljava/lang/Object;ZLjava/lang/Object;JLjava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011313233(Ljava/lang/Object;ZLjava/lang/Object;JLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0113133(Ljava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01131330(Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public static native n01131333(Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01132(Ljava/lang/Object;)J
.end method

.method public static native n011320(Ljava/lang/Object;J)V
.end method

.method public static native n011321(Ljava/lang/Object;J)Z
.end method

.method public static native n0113211(Ljava/lang/Object;JI)I
.end method

.method public static native n01132110(Ljava/lang/Object;DII)V
.end method

.method public static native n01132111(Ljava/lang/Object;DII)I
.end method

.method public static native n0113211130(Ljava/lang/Object;DIIILjava/lang/Object;)V
.end method

.method public static native n0113211131(Ljava/lang/Object;DIIILjava/lang/Object;)I
.end method

.method public static native n01132132(Ljava/lang/Object;JILjava/lang/Object;)J
.end method

.method public static native n011322(Ljava/lang/Object;J)J
.end method

.method public static native n0113220(Ljava/lang/Object;DD)V
.end method

.method public static native n0113222(Ljava/lang/Object;JJ)J
.end method

.method public static native n0113222130(Ljava/lang/Object;JJJILjava/lang/Object;)V
.end method

.method public static native n01132233(Ljava/lang/Object;JJLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011323(Ljava/lang/Object;J)Ljava/lang/Object;
.end method

.method public static native n0113230(Ljava/lang/Object;JLjava/lang/Object;)V
.end method

.method public static native n0113231(Ljava/lang/Object;JLjava/lang/Object;)I
.end method

.method public static native n01132313113130(Ljava/lang/Object;JLjava/lang/Object;ILjava/lang/Object;IILjava/lang/Object;ILjava/lang/Object;)V
.end method

.method public static native n0113232(Ljava/lang/Object;JLjava/lang/Object;)J
.end method

.method public static native n0113233(Ljava/lang/Object;JLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01132331(Ljava/lang/Object;JLjava/lang/Object;Ljava/lang/Object;)Z
.end method

.method public static native n011323313(Ljava/lang/Object;JLjava/lang/Object;Ljava/lang/Object;I)Ljava/lang/Object;
.end method

.method public static native n01132333(Ljava/lang/Object;JLjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011323331(Ljava/lang/Object;JLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Z
.end method

.method public static native n01133(Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011330(Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public static native n011331(Ljava/lang/Object;Ljava/lang/Object;)I
.end method

.method public static native n0113311(Ljava/lang/Object;Ljava/lang/Object;I)Z
.end method

.method public static native n01133110(Ljava/lang/Object;Ljava/lang/Object;ZI)V
.end method

.method public static native n01133111(Ljava/lang/Object;Ljava/lang/Object;II)I
.end method

.method public static native n011331110(Ljava/lang/Object;Ljava/lang/Object;IIZ)V
.end method

.method public static native n011331111(Ljava/lang/Object;Ljava/lang/Object;III)I
.end method

.method public static native n0113311110(Ljava/lang/Object;Ljava/lang/Object;FFIF)V
.end method

.method public static native n011331111131(Ljava/lang/Object;Ljava/lang/Object;FIFFFLjava/lang/Object;)F
.end method

.method public static native n0113311113(Ljava/lang/Object;Ljava/lang/Object;ZZZZ)Ljava/lang/Object;
.end method

.method public static native n01133111133(Ljava/lang/Object;Ljava/lang/Object;IIIILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011331113(Ljava/lang/Object;Ljava/lang/Object;ZII)Ljava/lang/Object;
.end method

.method public static native n0113311130(Ljava/lang/Object;Ljava/lang/Object;IIILjava/lang/Object;)V
.end method

.method public static native n0113311131(Ljava/lang/Object;Ljava/lang/Object;IIILjava/lang/Object;)I
.end method

.method public static native n0113311133(Ljava/lang/Object;Ljava/lang/Object;ZIILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01133112(Ljava/lang/Object;Ljava/lang/Object;ZZ)J
.end method

.method public static native n011331123(Ljava/lang/Object;Ljava/lang/Object;IIJ)Ljava/lang/Object;
.end method

.method public static native n01133113(Ljava/lang/Object;Ljava/lang/Object;ZI)Ljava/lang/Object;
.end method

.method public static native n011331131(Ljava/lang/Object;Ljava/lang/Object;IILjava/lang/Object;)I
.end method

.method public static native n01133113111130(Ljava/lang/Object;Ljava/lang/Object;IILjava/lang/Object;ZZZZLjava/lang/Object;)V
.end method

.method public static native n011331132(Ljava/lang/Object;Ljava/lang/Object;IILjava/lang/Object;)J
.end method

.method public static native n011331133(Ljava/lang/Object;Ljava/lang/Object;IILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0113312(Ljava/lang/Object;Ljava/lang/Object;I)J
.end method

.method public static native n0113313(Ljava/lang/Object;Ljava/lang/Object;Z)Ljava/lang/Object;
.end method

.method public static native n01133130(Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;)V
.end method

.method public static native n01133131(Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;)Z
.end method

.method public static native n0113313131(Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;ILjava/lang/Object;)Z
.end method

.method public static native n01133133(Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011331330(Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public static native n011331333(Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0113313331(Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)I
.end method

.method public static native n011332(Ljava/lang/Object;Ljava/lang/Object;)D
.end method

.method public static native n0113320(Ljava/lang/Object;Ljava/lang/Object;J)V
.end method

.method public static native n0113321(Ljava/lang/Object;Ljava/lang/Object;J)Z
.end method

.method public static native n01133210(Ljava/lang/Object;Ljava/lang/Object;JZ)V
.end method

.method public static native n011332133(Ljava/lang/Object;Ljava/lang/Object;DILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0113322(Ljava/lang/Object;Ljava/lang/Object;J)J
.end method

.method public static native n0113323(Ljava/lang/Object;Ljava/lang/Object;J)Ljava/lang/Object;
.end method

.method public static native n01133233(Ljava/lang/Object;Ljava/lang/Object;JLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011333(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0113330(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public static native n0113331(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)I
.end method

.method public static native n01133310(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Z)V
.end method

.method public static native n01133311(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Z)Z
.end method

.method public static native n011333111(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;II)I
.end method

.method public static native n01133311131(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;IIILjava/lang/Object;)I
.end method

.method public static native n011333113(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;II)Ljava/lang/Object;
.end method

.method public static native n0113331131(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;IILjava/lang/Object;)I
.end method

.method public static native n01133313(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Z)Ljava/lang/Object;
.end method

.method public static native n011333130(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;)V
.end method

.method public static native n011333131(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;)I
.end method

.method public static native n011333133(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0113331333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0113331333112(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;II)J
.end method

.method public static native n0113332(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)J
.end method

.method public static native n01133323(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;J)Ljava/lang/Object;
.end method

.method public static native n0113333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01133330(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public static native n01133331(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Z
.end method

.method public static native n011333310(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V
.end method

.method public static native n0113333133(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0113333133133(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01133331333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01133333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011333331(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)I
.end method

.method public static native n01133333133133(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011333331333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011333333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0113333333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01133333333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n011333333333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n0113333333333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public static native n01133333333333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method private static ᵢˋ(Landroid/content/Context;)Landroid/app/Application;
    .locals 2

    .prologue
    .line 81
    :try_start_0
    sget-object v0, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;

    if-nez v0, :cond_0

    .line 82
    invoke-virtual {p0}, Landroid/content/Context;->getClassLoader()Ljava/lang/ClassLoader;

    move-result-object v0

    .line 83
    if-eqz v0, :cond_0

    .line 84
    sget-object v1, Lcom/stub/StubApp;->strEntryApplication:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/ClassLoader;->loadClass(Ljava/lang/String;)Ljava/lang/Class;

    move-result-object v0

    .line 85
    if-eqz v0, :cond_0

    .line 86
    invoke-virtual {v0}, Ljava/lang/Class;->newInstance()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Landroid/app/Application;

    sput-object v0, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 92
    :cond_0
    :goto_0
    sget-object v0, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;

    return-object v0

    :catch_0
    move-exception v0

    goto :goto_0
.end method

.method private static ᵢˋ(Ljava/lang/String;ZZ)Ljava/lang/String;
    .locals 3

    .prologue
    .line 211
    sget-object v0, Lcom/stub/StubApp;->ᵢˏ:Ljava/lang/String;

    .line 212
    sget v1, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v2, 0x17

    if-ge v1, v2, :cond_0

    .line 213
    invoke-virtual {p0}, Ljava/lang/String;->hashCode()I

    move-result v1

    .line 214
    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    .line 216
    :cond_0
    if-eqz p1, :cond_1

    if-nez p2, :cond_1

    .line 217
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, "_64.so"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    .line 222
    :goto_0
    return-object v0

    .line 219
    :cond_1
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, ".so"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    goto :goto_0
.end method


# virtual methods
.method protected final attachBaseContext(Landroid/content/Context;)V
    .locals 8

    .prologue
    const/4 v7, 0x1

    const/4 v6, 0x0

    .line 126
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    .line 127
    invoke-super {p0, p1}, Landroid/app/Application;->attachBaseContext(Landroid/content/Context;)V

    .line 128
    invoke-static {}, Lcom/qihoo/util/ᵢˏ;->ᵢˎ()V

    .line 129
    sput-object p1, Lcom/stub/StubApp;->ᵢˑ:Landroid/content/Context;

    .line 130
    sget-object v0, Lcom/stub/StubApp;->ᵢˋ:Landroid/app/Application;

    if-nez v0, :cond_0

    .line 131
    sput-object p0, Lcom/stub/StubApp;->ᵢˋ:Landroid/app/Application;

    .line 133
    :cond_0
    sget-object v0, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;

    if-nez v0, :cond_6

    .line 135
    invoke-static {}, Lcom/qihoo/util/ᵢˏ;->ᵢˋ()Z

    move-result v0

    invoke-static {v0}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v3

    .line 136
    invoke-static {v6}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v0

    .line 137
    invoke-static {v6}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v1

    .line 138
    sget-object v2, Landroid/os/Build;->CPU_ABI:Ljava/lang/String;

    const-string v4, "64"

    invoke-virtual {v2, v4}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v2

    if-nez v2, :cond_1

    sget-object v2, Landroid/os/Build;->CPU_ABI2:Ljava/lang/String;

    const-string v4, "64"

    invoke-virtual {v2, v4}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v2

    if-eqz v2, :cond_2

    .line 139
    :cond_1
    invoke-static {v7}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v0

    .line 141
    :cond_2
    sget-object v2, Landroid/os/Build;->CPU_ABI:Ljava/lang/String;

    const-string v4, "mips"

    invoke-virtual {v2, v4}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v2

    if-nez v2, :cond_3

    sget-object v2, Landroid/os/Build;->CPU_ABI2:Ljava/lang/String;

    const-string v4, "mips"

    invoke-virtual {v2, v4}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v2

    if-eqz v2, :cond_4

    .line 142
    :cond_3
    invoke-static {v7}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v1

    .line 144
    :cond_4
    invoke-virtual {v3}, Ljava/lang/Boolean;->booleanValue()Z

    move-result v2

    if-eqz v2, :cond_5

    sget-boolean v2, Lcom/stub/StubApp;->needX86Bridge:Z

    if-eqz v2, :cond_5

    .line 145
    const-string v2, "X86Bridge"

    invoke-static {v2}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    .line 146
    :cond_5
    sget-boolean v2, Lcom/stub/StubApp;->loadFromLib:Z

    if-eqz v2, :cond_a

    .line 147
    invoke-virtual {v3}, Ljava/lang/Boolean;->booleanValue()Z

    move-result v0

    if-eqz v0, :cond_9

    sget-boolean v0, Lcom/stub/StubApp;->needX86Bridge:Z

    if-nez v0, :cond_9

    .line 148
    const-string v0, "jiagu_x86"

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    .line 189
    :cond_6
    :goto_0
    sget-object v0, Lcom/stub/StubApp;->ᵢˋ:Landroid/app/Application;

    invoke-static {v0}, Lcom/stub/StubApp;->interface5(Landroid/app/Application;)V

    .line 190
    sget-object v0, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;

    if-nez v0, :cond_8

    .line 191
    invoke-static {p1}, Lcom/stub/StubApp;->ᵢˋ(Landroid/content/Context;)Landroid/app/Application;

    move-result-object v0

    sput-object v0, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;

    .line 192
    sget-object v0, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;

    if-eqz v0, :cond_10

    .line 194
    :try_start_0
    const-class v0, Landroid/app/Application;

    const-string v1, "attach"

    const/4 v2, 0x1

    new-array v2, v2, [Ljava/lang/Class;

    const/4 v3, 0x0

    const-class v4, Landroid/content/Context;

    aput-object v4, v2, v3

    invoke-virtual {v0, v1, v2}, Ljava/lang/Class;->getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;

    move-result-object v0

    .line 195
    if-eqz v0, :cond_7

    .line 196
    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Ljava/lang/reflect/Method;->setAccessible(Z)V

    .line 197
    sget-object v1, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;

    const/4 v2, 0x1

    new-array v2, v2, [Ljava/lang/Object;

    const/4 v3, 0x0

    aput-object p1, v2, v3

    invoke-virtual {v0, v1, v2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 202
    :cond_7
    sget-object v0, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;

    invoke-static {v0, p1}, Lcom/stub/StubApp;->interface8(Landroid/app/Application;Landroid/content/Context;)Z

    .line 208
    :cond_8
    :goto_1
    return-void

    .line 150
    :cond_9
    const-string v0, "jiagu"

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    goto :goto_0

    .line 153
    :cond_a
    invoke-virtual {p1}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v2

    invoke-virtual {v2}, Ljava/io/File;->getParentFile()Ljava/io/File;

    move-result-object v2

    invoke-virtual {v2}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;

    move-result-object v2

    .line 155
    :try_start_1
    invoke-virtual {p1}, Landroid/content/Context;->getFilesDir()Ljava/io/File;

    move-result-object v4

    invoke-virtual {v4}, Ljava/io/File;->getParentFile()Ljava/io/File;

    move-result-object v4

    invoke-virtual {v4}, Ljava/io/File;->getCanonicalPath()Ljava/lang/String;
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_1

    move-result-object v2

    .line 159
    :goto_2
    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v4, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    const-string v4, "/.jiagu"

    invoke-virtual {v2, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    .line 160
    invoke-virtual {v0}, Ljava/lang/Boolean;->booleanValue()Z

    move-result v4

    invoke-virtual {v1}, Ljava/lang/Boolean;->booleanValue()Z

    move-result v5

    invoke-static {v2, v4, v5}, Lcom/stub/StubApp;->ᵢˋ(Ljava/lang/String;ZZ)Ljava/lang/String;

    move-result-object v4

    sput-object v4, Lcom/stub/StubApp;->ᵢᴵ:Ljava/lang/String;

    .line 161
    invoke-static {v2, v6, v6}, Lcom/stub/StubApp;->ᵢˋ(Ljava/lang/String;ZZ)Ljava/lang/String;

    move-result-object v4

    sput-object v4, Lcom/stub/StubApp;->ᵢי:Ljava/lang/String;

    .line 162
    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v4, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    sget-object v5, Ljava/io/File;->separator:Ljava/lang/String;

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    sget-object v5, Lcom/stub/StubApp;->ᵢי:Ljava/lang/String;

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    sput-object v4, Lcom/stub/StubApp;->ᵢـ:Ljava/lang/String;

    .line 163
    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v4, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    sget-object v5, Ljava/io/File;->separator:Ljava/lang/String;

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    sget-object v5, Lcom/stub/StubApp;->ᵢᴵ:Ljava/lang/String;

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    sput-object v4, Lcom/stub/StubApp;->ᵢٴ:Ljava/lang/String;

    .line 164
    sput-object v2, Lcom/stub/StubApp;->ᵢᐧ:Ljava/lang/String;

    .line 165
    invoke-virtual {v1}, Ljava/lang/Boolean;->booleanValue()Z

    move-result v4

    if-eqz v4, :cond_b

    .line 166
    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    sget-object v5, Lcom/stub/StubApp;->ᵢˏ:Ljava/lang/String;

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    const-string v5, "_mips.so"

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    sget-object v5, Lcom/stub/StubApp;->ᵢי:Ljava/lang/String;

    invoke-static {p1, v4, v2, v5}, Lcom/qihoo/util/ᵢˏ;->ᵢˋ(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Z

    .line 172
    :goto_3
    invoke-virtual {v0}, Ljava/lang/Boolean;->booleanValue()Z

    move-result v0

    if-eqz v0, :cond_f

    invoke-virtual {v1}, Ljava/lang/Boolean;->booleanValue()Z

    move-result v0

    if-nez v0, :cond_f

    .line 174
    invoke-virtual {v3}, Ljava/lang/Boolean;->booleanValue()Z

    move-result v0

    if-eqz v0, :cond_d

    sget-boolean v0, Lcom/stub/StubApp;->needX86Bridge:Z

    if-nez v0, :cond_d

    .line 175
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    sget-object v1, Lcom/stub/StubApp;->ᵢˏ:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, "_x64.so"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    sget-object v1, Lcom/stub/StubApp;->ᵢᴵ:Ljava/lang/String;

    invoke-static {p1, v0, v2, v1}, Lcom/qihoo/util/ᵢˏ;->ᵢˋ(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Z

    move-result v0

    .line 179
    :goto_4
    if-eqz v0, :cond_e

    .line 180
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, "/"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    sget-object v1, Lcom/stub/StubApp;->ᵢᴵ:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/System;->load(Ljava/lang/String;)V

    goto/16 :goto_0

    .line 167
    :cond_b
    invoke-virtual {v3}, Ljava/lang/Boolean;->booleanValue()Z

    move-result v4

    if-eqz v4, :cond_c

    sget-boolean v4, Lcom/stub/StubApp;->needX86Bridge:Z

    if-nez v4, :cond_c

    .line 168
    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    sget-object v5, Lcom/stub/StubApp;->ᵢˏ:Ljava/lang/String;

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    const-string v5, "_x86.so"

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    sget-object v5, Lcom/stub/StubApp;->ᵢי:Ljava/lang/String;

    invoke-static {p1, v4, v2, v5}, Lcom/qihoo/util/ᵢˏ;->ᵢˋ(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Z

    goto :goto_3

    .line 170
    :cond_c
    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    sget-object v5, Lcom/stub/StubApp;->ᵢˏ:Ljava/lang/String;

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    const-string v5, ".so"

    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    sget-object v5, Lcom/stub/StubApp;->ᵢי:Ljava/lang/String;

    invoke-static {p1, v4, v2, v5}, Lcom/qihoo/util/ᵢˏ;->ᵢˋ(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Z

    goto/16 :goto_3

    .line 177
    :cond_d
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    sget-object v1, Lcom/stub/StubApp;->ᵢˏ:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, "_a64.so"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    sget-object v1, Lcom/stub/StubApp;->ᵢᴵ:Ljava/lang/String;

    invoke-static {p1, v0, v2, v1}, Lcom/qihoo/util/ᵢˏ;->ᵢˋ(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Z

    move-result v0

    goto :goto_4

    .line 182
    :cond_e
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, "/"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    sget-object v1, Lcom/stub/StubApp;->ᵢי:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/System;->load(Ljava/lang/String;)V

    goto/16 :goto_0

    .line 184
    :cond_f
    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v0, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, "/"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    sget-object v1, Lcom/stub/StubApp;->ᵢי:Ljava/lang/String;

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Ljava/lang/System;->load(Ljava/lang/String;)V

    goto/16 :goto_0

    .line 199
    :catch_0
    move-exception v0

    .line 200
    new-instance v1, Ljava/lang/RuntimeException;

    const-string v2, "Failed to call attachBaseContext."

    invoke-direct {v1, v2, v0}, Ljava/lang/RuntimeException;-><init>(Ljava/lang/String;Ljava/lang/Throwable;)V

    throw v1

    .line 204
    :cond_10
    invoke-static {v7}, Ljava/lang/System;->exit(I)V

    goto/16 :goto_1

    :catch_1
    move-exception v4

    goto/16 :goto_2
.end method

.method public native declared-synchronized n1100()V
.end method

.method public native declared-synchronized n1101()Z
.end method

.method public native declared-synchronized n11010(Z)V
.end method

.method public native declared-synchronized n11011(B)Z
.end method

.method public native declared-synchronized n1101110(ZII)V
.end method

.method public native declared-synchronized n11011130(ZIILjava/lang/Object;)V
.end method

.method public native declared-synchronized n1101130(IILjava/lang/Object;)V
.end method

.method public native declared-synchronized n11011310(ZILjava/lang/Object;I)V
.end method

.method public native declared-synchronized n110120(IJ)V
.end method

.method public native declared-synchronized n11013(I)Ljava/lang/Object;
.end method

.method public native declared-synchronized n110130(ILjava/lang/Object;)V
.end method

.method public native declared-synchronized n1101321(ILjava/lang/Object;J)Z
.end method

.method public native declared-synchronized n1101330(ILjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native declared-synchronized n1102()J
.end method

.method public native declared-synchronized n11020(J)V
.end method

.method public native declared-synchronized n11021(J)Z
.end method

.method public native declared-synchronized n11023(J)Ljava/lang/Object;
.end method

.method public native declared-synchronized n110233(JLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native declared-synchronized n1103()Ljava/lang/Object;
.end method

.method public native declared-synchronized n11030(Ljava/lang/Object;)V
.end method

.method public native declared-synchronized n11031(Ljava/lang/Object;)Z
.end method

.method public native declared-synchronized n110310(Ljava/lang/Object;Z)V
.end method

.method public native declared-synchronized n110311(Ljava/lang/Object;I)Z
.end method

.method public native declared-synchronized n1103110(Ljava/lang/Object;II)V
.end method

.method public native declared-synchronized n1103111(Ljava/lang/Object;II)I
.end method

.method public native declared-synchronized n110323(Ljava/lang/Object;J)Ljava/lang/Object;
.end method

.method public native declared-synchronized n11033(Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native declared-synchronized n110331(Ljava/lang/Object;Ljava/lang/Object;)Z
.end method

.method public native declared-synchronized n110333(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native declared-synchronized n1103333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n1110()V
.end method

.method public native n1111()I
.end method

.method public native n11110(B)V
.end method

.method public native n11111(Z)I
.end method

.method public native n111110(IZ)V
.end method

.method public native n111111(IZ)Z
.end method

.method public native n1111110(III)V
.end method

.method public native n1111111(III)Z
.end method

.method public native n11111110(IIII)V
.end method

.method public native n11111111(IIII)Z
.end method

.method public native n111111110(ZIIII)V
.end method

.method public native n1111111110(IIIIII)V
.end method

.method public native n11111111110(IIIIIII)V
.end method

.method public native n1111111111111(IIIIIIIII)Z
.end method

.method public native n11111111111111130(ZZIIZZZIIZZZLjava/lang/Object;)V
.end method

.method public native n1111111113(IIIIZZ)Ljava/lang/Object;
.end method

.method public native n111111113(IIIIZ)Ljava/lang/Object;
.end method

.method public native n11111111330(IIIIZLjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n11111113(ISBI)Ljava/lang/Object;
.end method

.method public native n1111113(CCI)Ljava/lang/Object;
.end method

.method public native n11111130(IIILjava/lang/Object;)V
.end method

.method public native n111111330(IIILjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n111111331(ZZZLjava/lang/Object;Ljava/lang/Object;)Z
.end method

.method public native n1111120(IIJ)V
.end method

.method public native n111113(II)Ljava/lang/Object;
.end method

.method public native n1111130(IILjava/lang/Object;)V
.end method

.method public native n1111131(ZZLjava/lang/Object;)Z
.end method

.method public native n11111310(ZILjava/lang/Object;I)V
.end method

.method public native n11111311(ZZLjava/lang/Object;Z)Z
.end method

.method public native n1111131130(IILjava/lang/Object;ZZLjava/lang/Object;)V
.end method

.method public native n111113131(ZZLjava/lang/Object;ZLjava/lang/Object;)Z
.end method

.method public native n11111320(IZLjava/lang/Object;J)V
.end method

.method public native n11111330(IILjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n11111331(ZZLjava/lang/Object;Ljava/lang/Object;)Z
.end method

.method public native n111113311(ZZLjava/lang/Object;Ljava/lang/Object;Z)Z
.end method

.method public native n11111333(IILjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n1111133311(ZZLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Z)Z
.end method

.method public native n11112(I)J
.end method

.method public native n111120(IJ)V
.end method

.method public native n11112110(IJZZ)V
.end method

.method public native n111122(BJ)J
.end method

.method public native n1111222(BJJ)J
.end method

.method public native n111123(IJ)Ljava/lang/Object;
.end method

.method public native n1111230(IJLjava/lang/Object;)V
.end method

.method public native n1111233(IJLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n11112330(IJLjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n11112333(IJLjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n11113(I)Ljava/lang/Object;
.end method

.method public native n111130(ILjava/lang/Object;)V
.end method

.method public native n111131(ILjava/lang/Object;)Z
.end method

.method public native n1111310(ILjava/lang/Object;Z)V
.end method

.method public native n1111311(ZLjava/lang/Object;Z)Z
.end method

.method public native n11113110(ILjava/lang/Object;IZ)V
.end method

.method public native n11113111(ILjava/lang/Object;IZ)Z
.end method

.method public native n111131130(ILjava/lang/Object;ZZLjava/lang/Object;)V
.end method

.method public native n1111313(ILjava/lang/Object;Z)Ljava/lang/Object;
.end method

.method public native n1111320(ILjava/lang/Object;J)V
.end method

.method public native n1111323(ILjava/lang/Object;J)Ljava/lang/Object;
.end method

.method public native n11113230(ZLjava/lang/Object;JLjava/lang/Object;)V
.end method

.method public native n111133(ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n1111330(ILjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n11113310(ILjava/lang/Object;Ljava/lang/Object;Z)V
.end method

.method public native n11113311(ILjava/lang/Object;Ljava/lang/Object;I)Z
.end method

.method public native n11113313(ILjava/lang/Object;Ljava/lang/Object;Z)Ljava/lang/Object;
.end method

.method public native n11113330(ILjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n1111333120(ILjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;IJ)V
.end method

.method public native n11113333(ILjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n111133330(ILjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n1112()J
.end method

.method public native n11120(J)V
.end method

.method public native n11121(J)I
.end method

.method public native n111210(JZ)V
.end method

.method public native n111211(JI)I
.end method

.method public native n1112110(JII)V
.end method

.method public native n111211320(JIILjava/lang/Object;D)V
.end method

.method public native n1112113220(JIILjava/lang/Object;DD)V
.end method

.method public native n111211330(JIILjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n111212(JI)J
.end method

.method public native n1112122(JIJ)J
.end method

.method public native n11121222(JIDD)J
.end method

.method public native n111212230(JBJJLjava/lang/Object;)V
.end method

.method public native n11121310(JZLjava/lang/Object;Z)V
.end method

.method public native n11121312(JILjava/lang/Object;Z)J
.end method

.method public native n1112132(JILjava/lang/Object;)J
.end method

.method public native n11121322(JILjava/lang/Object;J)J
.end method

.method public native n11122(J)J
.end method

.method public native n111220(JJ)V
.end method

.method public native n111221(JJ)Z
.end method

.method public native n1112210(JJZ)V
.end method

.method public native n11122110(JJZZ)V
.end method

.method public native n11122111112(JJIIIIZ)J
.end method

.method public native n111221111133(JJIZZZZLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n1112211112123(JJIZZZJFD)Ljava/lang/Object;
.end method

.method public native n1112211113(JJIZZB)Ljava/lang/Object;
.end method

.method public native n11122111133(JJIZZZLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n1112211123(JJIZZD)Ljava/lang/Object;
.end method

.method public native n11122112(JJIZ)J
.end method

.method public native n1112212(JJI)D
.end method

.method public native n111222(JJ)J
.end method

.method public native n1112220(JJD)V
.end method

.method public native n1112221(JJJ)Z
.end method

.method public native n11122210(JJDZ)V
.end method

.method public native n11122212(JJJZ)J
.end method

.method public native n1112222(JJD)J
.end method

.method public native n11122222(JJJJ)J
.end method

.method public native n111222222(JJJJJ)D
.end method

.method public native n111222223(JJJJJ)Ljava/lang/Object;
.end method

.method public native n11122223(JJJJ)Ljava/lang/Object;
.end method

.method public native n1112222330(JJJJLjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n1112223(JJJ)Ljava/lang/Object;
.end method

.method public native n11122230(JJJLjava/lang/Object;)V
.end method

.method public native n111223(JJ)Ljava/lang/Object;
.end method

.method public native n1112230(JJLjava/lang/Object;)V
.end method

.method public native n11122310(JJLjava/lang/Object;Z)V
.end method

.method public native n111223130(JJLjava/lang/Object;ILjava/lang/Object;)V
.end method

.method public native n111223133(JJLjava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n1112232(JJLjava/lang/Object;)J
.end method

.method public native n1112233(JJLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n11122330(JJLjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n11122333(JJLjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n11123(J)Ljava/lang/Object;
.end method

.method public native n111230(JLjava/lang/Object;)V
.end method

.method public native n111231(JLjava/lang/Object;)Z
.end method

.method public native n11123110(JLjava/lang/Object;FF)V
.end method

.method public native n11123111(JLjava/lang/Object;II)Z
.end method

.method public native n1112313(JLjava/lang/Object;I)Ljava/lang/Object;
.end method

.method public native n11123131130(JLjava/lang/Object;ILjava/lang/Object;IILjava/lang/Object;)V
.end method

.method public native n11123133(JLjava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n111232(JLjava/lang/Object;)J
.end method

.method public native n1112320(DLjava/lang/Object;D)V
.end method

.method public native n11123220(JLjava/lang/Object;DD)V
.end method

.method public native n11123230(DLjava/lang/Object;DLjava/lang/Object;)V
.end method

.method public native n111233(JLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n1112330(JLjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n11123310(JLjava/lang/Object;Ljava/lang/Object;F)V
.end method

.method public native n11123313(JLjava/lang/Object;Ljava/lang/Object;Z)Ljava/lang/Object;
.end method

.method public native n1112332(DLjava/lang/Object;Ljava/lang/Object;)D
.end method

.method public native n11123320(JLjava/lang/Object;Ljava/lang/Object;D)V
.end method

.method public native n1112333(JLjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n11123330(JLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n111233310(JLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Z)V
.end method

.method public native n11123333(JLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n1113()Ljava/lang/Object;
.end method

.method public native n11130(Ljava/lang/Object;)V
.end method

.method public native n11131(Ljava/lang/Object;)Z
.end method

.method public native n111310(Ljava/lang/Object;Z)V
.end method

.method public native n111311(Ljava/lang/Object;I)Z
.end method

.method public native n1113110(Ljava/lang/Object;II)V
.end method

.method public native n1113111(Ljava/lang/Object;II)I
.end method

.method public native n11131110(Ljava/lang/Object;III)V
.end method

.method public native n11131111(Ljava/lang/Object;IIZ)Z
.end method

.method public native n111311110(Ljava/lang/Object;IIZZ)V
.end method

.method public native n111311111(Ljava/lang/Object;IIIZ)Z
.end method

.method public native n1113111111(Ljava/lang/Object;ZIIII)Z
.end method

.method public native n1113111111110(Ljava/lang/Object;IIIIIIII)V
.end method

.method public native n1113111130(Ljava/lang/Object;IIIILjava/lang/Object;)V
.end method

.method public native n111311130(Ljava/lang/Object;IZZLjava/lang/Object;)V
.end method

.method public native n1113113(Ljava/lang/Object;ZI)Ljava/lang/Object;
.end method

.method public native n11131130(Ljava/lang/Object;IILjava/lang/Object;)V
.end method

.method public native n11131133(Ljava/lang/Object;IILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n111312(Ljava/lang/Object;Z)J
.end method

.method public native n1113120(Ljava/lang/Object;IJ)V
.end method

.method public native n11131230(Ljava/lang/Object;IJLjava/lang/Object;)V
.end method

.method public native n11131233(Ljava/lang/Object;IJLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n111312330(Ljava/lang/Object;IJLjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n111312333(Ljava/lang/Object;IJLjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n1113123330(Ljava/lang/Object;IJLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n111313(Ljava/lang/Object;I)Ljava/lang/Object;
.end method

.method public native n1113130(Ljava/lang/Object;ILjava/lang/Object;)V
.end method

.method public native n11131310(Ljava/lang/Object;ILjava/lang/Object;I)V
.end method

.method public native n111313130(Ljava/lang/Object;ZLjava/lang/Object;ILjava/lang/Object;)V
.end method

.method public native n1113133(Ljava/lang/Object;ILjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n11131330(Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n111313310(Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;Z)V
.end method

.method public native n11131333(Ljava/lang/Object;ZLjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n111313330(Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n1113133333333330(Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n11132(Ljava/lang/Object;)J
.end method

.method public native n111320(Ljava/lang/Object;J)V
.end method

.method public native n111321(Ljava/lang/Object;J)I
.end method

.method public native n1113210(Ljava/lang/Object;JI)V
.end method

.method public native n1113213(Ljava/lang/Object;JI)Ljava/lang/Object;
.end method

.method public native n111321320(Ljava/lang/Object;JILjava/lang/Object;J)V
.end method

.method public native n11132133(Ljava/lang/Object;JZLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n111322(Ljava/lang/Object;J)J
.end method

.method public native n1113220(Ljava/lang/Object;JJ)V
.end method

.method public native n11132210(Ljava/lang/Object;JJI)V
.end method

.method public native n1113223(Ljava/lang/Object;DD)Ljava/lang/Object;
.end method

.method public native n111322320(Ljava/lang/Object;JJLjava/lang/Object;J)V
.end method

.method public native n11132233(Ljava/lang/Object;JJLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n1113223310(Ljava/lang/Object;JJLjava/lang/Object;Ljava/lang/Object;I)V
.end method

.method public native n11132233110(Ljava/lang/Object;JJLjava/lang/Object;Ljava/lang/Object;IZ)V
.end method

.method public native n1113223320(Ljava/lang/Object;JJLjava/lang/Object;Ljava/lang/Object;J)V
.end method

.method public native n111322332110(Ljava/lang/Object;JJLjava/lang/Object;Ljava/lang/Object;JIZ)V
.end method

.method public native n111322333110(Ljava/lang/Object;JJLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;IZ)V
.end method

.method public native n111323(Ljava/lang/Object;J)Ljava/lang/Object;
.end method

.method public native n1113230(Ljava/lang/Object;JLjava/lang/Object;)V
.end method

.method public native n11132310(Ljava/lang/Object;JLjava/lang/Object;Z)V
.end method

.method public native n11132320(Ljava/lang/Object;JLjava/lang/Object;J)V
.end method

.method public native n1113233(Ljava/lang/Object;JLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n11132330(Ljava/lang/Object;JLjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n111323310(Ljava/lang/Object;JLjava/lang/Object;Ljava/lang/Object;Z)V
.end method

.method public native n1113233110(Ljava/lang/Object;JLjava/lang/Object;Ljava/lang/Object;IZ)V
.end method

.method public native n11132331210(Ljava/lang/Object;JLjava/lang/Object;Ljava/lang/Object;IJZ)V
.end method

.method public native n11132333(Ljava/lang/Object;JLjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n111323330(Ljava/lang/Object;JLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n11133(Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n111330(Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n111331(Ljava/lang/Object;Ljava/lang/Object;)Z
.end method

.method public native n1113310(Ljava/lang/Object;Ljava/lang/Object;Z)V
.end method

.method public native n11133110(Ljava/lang/Object;Ljava/lang/Object;ZI)V
.end method

.method public native n111331110(Ljava/lang/Object;Ljava/lang/Object;IIZ)V
.end method

.method public native n1113311111110(Ljava/lang/Object;Ljava/lang/Object;ZZZZZZZ)V
.end method

.method public native n111331113(Ljava/lang/Object;Ljava/lang/Object;ZZZ)Ljava/lang/Object;
.end method

.method public native n1113311230(Ljava/lang/Object;Ljava/lang/Object;IIJLjava/lang/Object;)V
.end method

.method public native n11133113(Ljava/lang/Object;Ljava/lang/Object;ZZ)Ljava/lang/Object;
.end method

.method public native n111331130(Ljava/lang/Object;Ljava/lang/Object;IILjava/lang/Object;)V
.end method

.method public native n1113312(Ljava/lang/Object;Ljava/lang/Object;Z)J
.end method

.method public native n1113313(Ljava/lang/Object;Ljava/lang/Object;Z)Ljava/lang/Object;
.end method

.method public native n11133130(Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;)V
.end method

.method public native n11133131(Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;)Z
.end method

.method public native n111331310(Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;Z)V
.end method

.method public native n11133133(Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n111331330(Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n111331333(Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n1113313330(Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n11133133330(Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n111332(Ljava/lang/Object;Ljava/lang/Object;)J
.end method

.method public native n1113320(Ljava/lang/Object;Ljava/lang/Object;J)V
.end method

.method public native n1113321(Ljava/lang/Object;Ljava/lang/Object;J)Z
.end method

.method public native n11133211(Ljava/lang/Object;Ljava/lang/Object;JI)Z
.end method

.method public native n11133221(Ljava/lang/Object;Ljava/lang/Object;JJ)Z
.end method

.method public native n1113322330(Ljava/lang/Object;Ljava/lang/Object;JJLjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n1113323(Ljava/lang/Object;Ljava/lang/Object;J)Ljava/lang/Object;
.end method

.method public native n11133230(Ljava/lang/Object;Ljava/lang/Object;JLjava/lang/Object;)V
.end method

.method public native n111332310(Ljava/lang/Object;Ljava/lang/Object;JLjava/lang/Object;Z)V
.end method

.method public native n11133231130(Ljava/lang/Object;Ljava/lang/Object;JLjava/lang/Object;IZLjava/lang/Object;)V
.end method

.method public native n111332320(Ljava/lang/Object;Ljava/lang/Object;JLjava/lang/Object;J)V
.end method

.method public native n111332330(Ljava/lang/Object;Ljava/lang/Object;JLjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n1113323311110(Ljava/lang/Object;Ljava/lang/Object;JLjava/lang/Object;Ljava/lang/Object;ZZZZ)V
.end method

.method public native n111333(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n1113330(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n1113331(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Z
.end method

.method public native n11133310(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V
.end method

.method public native n111333110(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;IZ)V
.end method

.method public native n111333113(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;IZ)Ljava/lang/Object;
.end method

.method public native n1113331130(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;IZLjava/lang/Object;)V
.end method

.method public native n11133311330(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;IZLjava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n111333120(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;IJ)V
.end method

.method public native n11133313(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Z)Ljava/lang/Object;
.end method

.method public native n111333130(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;)V
.end method

.method public native n1113331310(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;Z)V
.end method

.method public native n11133313110(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;IZ)V
.end method

.method public native n11133313330(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n111333133310(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V
.end method

.method public native n1113332(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)J
.end method

.method public native n11133320(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;J)V
.end method

.method public native n1113333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n11133330(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n11133331(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Z
.end method

.method public native n111333310(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V
.end method

.method public native n1113333133(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n111333313331110(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ILjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;III)V
.end method

.method public native n11133333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n111333330(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n111333331(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)I
.end method

.method public native n1113333310(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;I)V
.end method

.method public native n111333331110(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ZZZ)V
.end method

.method public native n111333331130(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;IILjava/lang/Object;)V
.end method

.method public native n1113333323133331310(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;JLjava/lang/Object;ZLjava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;ZLjava/lang/Object;Z)V
.end method

.method public native n111333333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n1113333330(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n1113333333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n11133333330(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n11133333333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n111333333330(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n111333333333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public native n1113333333330(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)V
.end method

.method public native n1113333333333(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
.end method

.method public final onCreate()V
    .locals 2

    .prologue
    .line 113
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    .line 114
    invoke-super {p0}, Landroid/app/Application;->onCreate()V

    .line 1103
    sget-object v0, Lcom/stub/StubApp;->ᵢˋ:Landroid/app/Application;

    invoke-virtual {v0}, Landroid/app/Application;->getBaseContext()Landroid/content/Context;

    move-result-object v0

    .line 1105
    :try_start_0
    sget-object v1, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;

    invoke-static {v1, v0}, Lcom/stub/StubApp;->interface7(Landroid/app/Application;Landroid/content/Context;)Z
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 117
    :goto_0
    sget-object v0, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;

    if-eqz v0, :cond_0

    .line 118
    sget-object v0, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;

    invoke-virtual {v0}, Landroid/app/Application;->onCreate()V

    .line 121
    :cond_0
    sget-object v0, Lcom/stub/StubApp;->ᵢˎ:Landroid/app/Application;

    invoke-static {v0}, Lcom/stub/StubApp;->interface21(Landroid/app/Application;)V

    .line 122
    return-void

    :catch_0
    move-exception v0

    goto :goto_0
.end method
