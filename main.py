"""Follow Elon - 主程序入口"""

from examples.basic_usage import main as run_example


def main():
    """主函数"""
    print("Follow Elon - X平台@elonmusk活动追踪程序")
    print("=" * 50)
    print()
    
    print("运行基础使用示例...")
    print("注意：需要设置TWITTER_API_KEY环境变量")
    print()
    
    # 运行基础示例
    run_example()


if __name__ == "__main__":
    main()
